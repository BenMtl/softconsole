from logsupport import ConsoleError
import logsupport
import time
import debug

ValueStores = {} # General store for named values storename:itemname accessed as ValueStore[storename].GetVal(itemname)
				# or GetVal([itemname]) for a nested name

def _normalizename(name):
	if isinstance(name, tuple):
		return list(name)
	elif isinstance(name, list):
		return name[:]
	elif isinstance(name, str):
		return name.split(':')
	else:
		logsupport.Logs.Log("Normalize name got strange input: ", name, severity=ConsoleError)
		return [name]

def InternalizeVarName(name):
	return name.split(':')

def ExternalizeVarName(name):
	n = name[0]
	for i in name[1:]:
		n = n + ':' + i
	return n

def PrettyVarName(store,name):
	p = store
	if isinstance(name,basestring):
		name = [name]
	for i in name:
		p = p + ':' + str(i)
	return p

def GetVal(name):
	n = _normalizename(name)
	return ValueStores[n[0]].GetVal(n[1:])

def SetVal(name,val, modifier = None):
	n = _normalizename(name)
	return ValueStores[n[0]].SetVal(n[1:],val, modifier)

def GetAttr(name):
	n = _normalizename(name)
	return ValueStores[n[0].GetAttr(n[1:])]

def AddAlert(name,a):
	n = _normalizename(name)
	return ValueStores[n[0]].AddAlert(n[1:],a)

def SetAttr(name,attr):
	n = _normalizename(name)
	return ValueStores[n[0]].SetAttr(n[1:],attr)

def GetValByAttr(name, attr):
	return ValueStores[name].GetValByAttr(attr)

def SetValByAttr(name, attr, val, modifier = None):
	return ValueStores[name].SetValByAttr(attr,val,modifier)

def BlockRefresh(name):
	ValueStores[name].BlockRefresh()

class StoreList(object):
	def __init__(self,parent):
		self.parent = parent
		self._List = []

	def __getitem__(self, item):
		return self._List[item]

	def __setitem__(self, key, value):
		debug.debugPrint('StoreTrack',
						 "StoreList: ", PrettyVarName(self.parent.enclstore.name, self.parent.name), '[', key, ']  Value: ', value)
		self._List[key] = value

	def __len__(self):
		return len(self._List)

	def append(self,val):
		debug.debugPrint('StoreTrack',
						 "AppendList: ", PrettyVarName(self.parent.enclstore.name, self.parent.name), '[', len(self._List), ']  Value: ', val)
		self._List.append(val)

	def __str__(self):
		return str(self._List)

def NewValueStore(store):
	if store.name in ValueStores:
		if isinstance(ValueStores[store.name],type(store)):
			return ValueStores[store.name]
		else:
			logsupport.Logs.Log("Incompatible store types for: "+store.name,severity=ConsoleError)
			return None
	else:
		ValueStores[store.name] = store
		return ValueStores[store.name]

class StoreItem(object):
	def __init__(self, name, initval, store = None, vt = None, Expires=9999999999999999.0, attribute=None):

		self._Value = None
		self.name = name
		self.Attribute = attribute
		self.SetTime = 0
		self.Expires = Expires
		self.Alerts = []
		if vt is None:
			self.Type = None if initval is None else type(initval)
		else:
			self.Type = vt
		self.enclstore = store
		self.UpdateVal(initval)


	@property
	def Value(self):
		return self._Value

	@Value.setter
	def Value(self, value):
		debug.debugPrint('StoreTrack', "Store: ", PrettyVarName(self.enclstore.name, self.name), ' Value: ', value)
		self._Value = value

	@Value.deleter
	def Value(self):
		print("deleter of x called")
		del self._Value

	def UpdateVal(self,val):
		if val == None:
			self.Value = None
		else:
			self.Value = val if self.Type is None else self.Type(val)
			self.SetTime = time.time()

	def UpdateArrayVal(self,index,val):
		if isinstance(self.Value, list):
			if index >= len(self.Value):
				for i in range(len(self.Value),index+1):
					self.Value.append(None)
			self.Value[index] = val if self.Type is None else self.Type(val)
		else:
			return # todo error
		self.SetTime = time.time()

class ValueStore(object):
	def __init__(self, name, refreshinterval = 0, itemtyp=StoreItem):
		self.name = name
		self.itemtyp = itemtyp
		self.fetchtime = 0 # time of last block refresh if handled as such
		self.refreshinterval = refreshinterval
		self.vars = {}
		self.attrs = {}
		self.attrnames = {}
		self.locked = False

	def _normalizename(self,name):
		if isinstance(name, list):
			return name[:]
		elif isinstance(name, tuple):
			return list(name)
		elif isinstance(name, str):
			return name.split(':')
		else:
			logsupport.Logs.Log("Normalize name got strange input: ",name,severity=ConsoleError)
			return [name]

	def _accessitem(self,n2):
		t = self.vars
		while len(n2) > 1:
			t = t[n2[0]]
			n2.pop(0)
		try:
			indx = int(n2[0])
			return (t, indx)
		except:
			return (t[n2[0]], None)

	def LockStore(self):
		self.locked = True

	def GetVal(self,name):
		if self.refreshinterval != 0 and time.time()>self.fetchtime+self.refreshinterval:
			self.BlockRefresh()
		try:
			n2 = self._normalizename(name)
			item, index = self._accessitem(n2)
			V = item.Value if index is None else item.Value[index]

			if item.Expires + item.SetTime < time.time():
				# value is stale
				return None
			else:
				return V
		except:
			logsupport.Logs.Log("Error accessing ", self.name, ":", str(name), severity=ConsoleError)
			return None

	def GetValByAttr(self, attr):
		return self.attrs[attr].Value

	def SetAttr(self,name,attr):
		try:
			n = self._normalizename(name)
			item, index = self._accessitem(n)
			if index is None:
				if item.Attribute is None:
					item.Attribute = attr
					self.attrs[attr] = item
					self.attrnames[attr] = name
				else:
					logsupport.Logs.Log("Attribute already set for ",self.name," new attr: ", attr)
			else:
				logsupport.Logs.Log("Can't set attribute on array element for ",self.name," new attr: ",attr)
		except:
			logsupport.Logs.Log("Attribute setting error", self.name, " new attr: ", attr)

	def AddAlert(self,name,a):
		try:
			if not isinstance(a,tuple):
				a = (a,None)
			n = self._normalizename(name)
			item, index = self._accessitem(n)
			if index is None:
				if a not in item.Alerts: # don't add twice
					item.Alerts.append(a)
			else:
				logsupport.Logs.Log("Can't set alert on array element for ", self.name)
		except Exception as e:
			logsupport.Logs.Log("Alert add error", self.name, " Exception: ", e)

	def SetType(self,name,type):
		try:
			n = self._normalizename(name)
			item, index = self._accessitem(n)
			if index is None:
				if item.Type is None:
					item.Type = type
				else:
					logsupport.Logs.Log("Type already set for ", self.name, " new type: ", type)
			else:
				logsupport.Logs.Log("Can't set Type on array element for ", self.name, " new type: ", type)
		except:
			logsupport.Logs.Log("Type setting error", self.name, " new type: ", type)

	def GetAttr(self,name):
		try:
			n2 = self._normalizename(name)
			item, index = self._accessitem(n2)
			return item.Attribute
		except:
			logsupport.Logs.Log("Error accessing attribute ", self.name, ":", str(name), severity=ConsoleError)
			return None

	def SimpleInit(self, nmlist, init):
		if self.itemtyp != StoreItem:
			logsupport.Logs.Log("Can't SimpleInit non-simple store: ",self.name, severity=ConsoleError)
			return # todo abort internal error
		if isinstance(nmlist, tuple) or isinstance(nmlist, list):
			self.vars = {}
			for n in nmlist:
				self.vars[n] = self.itemtyp(n, init, store=self)

	def SetVal(self,name, val, modifier = None):
		n2 = self._normalizename(name)
		n = n2[:]
		t = self.vars
		while len(n2) > 1:
			if n2[0] in t:
				t = t[n2[0]]
				n2.pop(0)
			else:
				if self.locked:
					logsupport.Logs.Log('Attempt to add element to locked store',self.name,n)
					return
				t[n2[0]] = {} if not isinstance(n2[1],int) else self.itemtyp(StoreList(t),val,store=self) # todo test
				t = t[n2[0]]
				n2.pop(0)
		if isinstance(n2[0], int):
			if isinstance(t,self.itemtyp):
				oldval = t.Value[n2[0]]
				t.UpdateArrayVal(n2[0],val)
			else: # need to create an itemtyp here since t is a dict presumably empty as temporary part of creating multilevel
				oldval = None
				if self.locked:
					logsupport.Logs.Log('Attempt to add element to locked store',self.name,n)
					return
				t = self.itemtyp(n2, StoreList(t),parent=self)
				t.UpdateArrayVal(n2[0],val)
			if val != oldval: # todo notify for array values? test whether this equality is what is wanted for arrays
				for notify in t.Alerts:
					notify[0](t,oldval,val,n2[0],notify[1],modifier)
		else:
			if n2[0] in t:
				oldval = t[n2[0]].Value
				# already exists
				t[n2[0]].UpdateVal(val)
			else:
				oldval = None
				t[n2[0]] = self.itemtyp(n,val,store=self)
			if val != oldval:
				for notify in t[n2[0]].Alerts:
					notify[0](t[n2[0]],oldval,val,notify[1],modifier)

	def SetValByAttr(self, attr, val, modifier = None):
		storeitem = self.attrs[attr]
		oldval = storeitem.Value
		storeitem.Value = val if storeitem.Type is None else storeitem.Type(val)
		for notify in storeitem.Alerts:
			notify[0](storeitem,oldval,val,notify[1], modifier)

	def items(self, parents=(), d=None):
		if d is None: d = self.vars
		for n, i in d.iteritems():
			if isinstance(i, dict):
				np = parents + (n,)
				for b in self.items(parents=np, d=i):
					yield b
			else:
				yield (parents + (n,))

	def __iter__(self):
		self.iternames = self.vars.keys()
		return self

	def next(self):
		try:
			return self.vars[self.iternames.pop(0)]
		except IndexError:
			raise StopIteration



	def Contains(self,name):
		n2 = self._normalizename(name)
		t = self.vars
		try:
			while len(n2) > 1:
				t = t[n2[0]]
				n2.pop(0)
			if isinstance(n2[0], int):
				# final is array
				return True if n2[0] < len(t.Value) else False
			else:
				return True if n2[0] in t else False
		except:
			return False

	def BlockRefresh(self):
		pass
