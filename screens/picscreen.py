import screen
import screens.__screens as screens
import pygame
import debug
import utilities
import time
import hw
import config
import threading, queue
import os
import PIL.Image
import logsupport
from logsupport import ConsoleWarning, ConsoleDetail

class PictureScreenDesc(screen.ScreenDesc):
	def __init__(self, screensection, screenname, Clocked=0):
		super().__init__(screensection, screenname, Clocked=1)
		debug.debugPrint('Screen', "Build Picture Screen")

		self.KeyList = None
		utilities.register_example("PictureScreen", self)

		screen.AddUndefaultedParams(self, screensection, picturedir="", picturetime=5, singlepic='')
		self.singlepicmode = self.singlepic != ''
		if self.singlepicmode:
			if self.singlepic[0] != '/':
				self.singlepic = os.path.dirname(config.sysStore.configfile) + '/' + self.singlepic
			logsupport.Logs.Log('Picture screen {} in single mode for {}'.format(self.name, self.singlepic))
			self.picturetime = 9999
		else:
			if self.picturedir == '':
				self.picturedir = os.path.dirname(config.sysStore.configfile) + '/pics'
			elif self.picturedir[0] != '/':
				self.picturedir = os.path.dirname(config.sysStore.configfile) + '/' + self.picturedir
			if '*' in self.picturedir: self.picturedir = self.picturedir.replace('*', config.sysStore.hostname)
			logsupport.Logs.Log('Picture screen {} in directory mode for {}'.format(self.name, self.picturedir))

		self.holdtime = 0
		self.blankpic = (pygame.Surface((1, 1)), 1, 1)
		self.picshowing = self.blankpic[0]
		self.woffset = 1
		self.hoffset = 1
		self.picture = '*none*'
		self.modtime = 0
		self.picqueue = queue.Queue(maxsize=1)
		self.DoSinglePic = threading.Event()
		self.DoSinglePic.set()
		self.queueingthread = threading.Thread(name=self.name + 'qthread',
											   target=[self.QueuePics, self.QueueSinglePic][self.singlepicmode],
											   daemon=True)
		self.queueingthread.start()

	def QueueSinglePic(self):
		while True:
			pictime = os.path.getmtime(self.singlepic)
			if pictime != self.modtime:
				self.modtime = pictime
				picdescr = self._preppic(self.singlepic)
				self.picqueue.put(('*single*', picdescr), block=True)
				self.holdtime = -1
			time.sleep(1)

	def QueuePics(self):
		issueerror = True
		reportedpics = []
		pictureset = []
		select = 0
		while True:
			dirtime = os.path.getmtime(self.picturedir)
			if dirtime != self.modtime:
				self.modtime = dirtime
				reportedpics = []
				pictureset = os.listdir(self.picturedir)
				picsettrimmed = pictureset.copy()
				for n in pictureset:
					if not n.endswith(('.jpg', '.JPG')):
						picsettrimmed.remove(n)
				pictureset = picsettrimmed
				pictureset.sort()
				logsupport.Logs.Log('Screen {} reset using {} pictures'.format(self.name, len(pictureset)))
				select = 0
			try:
				picture = pictureset[select]
			except IndexError:
				if len(pictureset) == 0:
					picture = '*Empty*'
					if issueerror:
						logsupport.Logs.Log("Empty picture directory for screen {}".format(self.name),
											severity=ConsoleWarning)
						issueerror = False
					select = -1
				else:
					issueerror = True
					picture = pictureset[0]
					select = 0

			if select == -1:
				picture = '*None*'
				picdescr = self.blankpic
			else:
				try:
					select += 1
					picdescr = self._preppic(self.picturedir + '/' + picture)
				except Exception as E:
					if picture not in reportedpics:
						logsupport.Logs.Log('Error processing picture {} ({})'.format(picture, E),
											severity=ConsoleWarning)
						reportedpics.append(picture)
					picdescr = self.blankpic
			self.picqueue.put((picture, picdescr), block=True)

	def InitDisplay(self, nav, specificrepaint=None):
		if not self.singlepicmode: self.holdtime = 0
		super().InitDisplay(nav)

	@staticmethod
	def _preppic(pic):
		rawp = pygame.image.load(pic)
		try:
			exif = PIL.Image.open(pic)._getexif()[274]
		except Exception:
			exif = 1
		rot = [0, 0, 0, 180, 0, 0, 270, 0, 90][exif]
		if rot != 0: rawp = pygame.transform.rotate(rawp, rot)
		ph = rawp.get_height()
		pw = rawp.get_width()
		vertratio = hw.screenheight / ph
		horizratio = hw.screenwidth / pw
		# one of these ratios will yield a scaled picture that is larger that the relevant screen size
		# so pick one and if it is less than the relevant screen dimension use it, otherwise it is the other one
		horizifvertscale = vertratio * pw
		if horizifvertscale < hw.screenwidth:
			scalefac = vertratio
		else:
			scalefac = horizratio
		picframed = pygame.transform.smoothscale(rawp, (int(scalefac * pw), int(scalefac * ph)))
		woffset = (hw.screenwidth - picframed.get_width()) // 2
		hoffset = (hw.screenheight - picframed.get_height()) // 2
		return picframed, woffset, hoffset

	def ScreenContentRepaint(self):
		if not self.Active:
			return  # handle race conditions where repaint queued just before screen switch

		self.holdtime -= 1
		if self.holdtime <= 0:
			# get new picture
			try:
				self.picture, picdescr = self.picqueue.get_nowait()
				self.holdtime = self.picturetime
				self.picshowing, self.woffset, self.hoffset = picdescr

			except queue.Empty:
				if not self.singlepicmode:  # normal case in single mode is nothing changed
					logsupport.Logs.Log('Picture not ready for screen {} holding {} ({})'.format(self.name,
																								 self.picture,
																								 self.holdtime),
										severity=ConsoleDetail)
		hw.screen.blit(self.picshowing, (self.woffset, self.hoffset))

screens.screentypes["Picture"] = PictureScreenDesc
