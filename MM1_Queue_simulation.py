import numpy as np
import rand
#from Queue import Queue

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class Schedule(object):
	"""docstring for Schedule"""
	def __init__(self, time, func, next=None):
		self.time = time
		self.func = func
		self.next = None


class Simulation(object):
	exp_scale = 10
	ids = 0
	S_pointer = None
	queue = None
	all_times = []
	#lmb = 0
	#Ts = 0


	def __init__(self, max_time, lmb, Ts):
		print("Init has been called")
		self.lmb = lmb
		self.queue = []
		self.Ts = Ts
		self.max_time = max_time
		self.rate = 0
		self.waiting_times = []
		self.service_times = []
		self.IAT = []

		self.queue_is_empty = False
		self.idleTime = 0 #used for calculating utilization

		self.departures = 0

		self.number_arrivals = 0.0

		self.gen_serivice_time = rand.randVar(1 / Ts)
		self.gen_arrival_time = rand.randVar(lmb)

		#self.start_simulation()
		#self.Ts = Ts
		



	#MODEL FOR CALANDER/SCHEDULE
	def print_cal(self, r):
		#print the calander for the purpose of debugging
		cstr = ""
		
		while(r != None):
			cstr += "-- [" + str(r.func) + " " + str(r.time) + "] -- "
			r = r.next
		print(cstr)

	def is_empty(self, r):
		#calander should never be empty
		if (r.next == None and r.time == 0) or r == None:
			return True

		return False


	def add_item(self, r, **k):
		#add item k into schedule r
		# k should be structured as a dict {"time": , "funct": pointer to function}

		if r == None:
			return Schedule(k["time"], k["func"], None)

		elif k["time"] < r.time:

			s = Schedule(k["time"], k["func"], r)
			s.next = r
			return s

		elif k["time"] == r.time:

			#k["time"] += 1

			#s = Schedule(k["time"] + 1, k["func"], r)
			#s.next = r
			return self.add_item( r, time = k["time"] + 1, func = k["func"])

		else:
			r.next = self.add_item( r.next, time = k["time"], func = k["func"])
			return r


	####END OF QUEUE FUNCTIONALITY


	def initializeState	(self):
		#add one single birth event in the system

		self.S_pointer = self.add_item(self.S_pointer, time=int(self.gen_arrival_time.exp()), func=self.birth)
		self.queue = []
	

	####EVENTS 
	def birth(self):
		print("Birth event has been called: ")
		#first add request in the queue and assign ts 
		self.queue_is_empty = True

		self.number_arrivals += 1

		if not self.queue: # If no requests waiting
			print("Assigning Service time immediatly")
			k =  int(self.gen_serivice_time.exp() * 100)

			self.service_times.append(k/100.0)	
			k += self.curr_time 

			self.queue.append({"Ts": k, "arrival": self.curr_time})
			#the service time -- Ts -- is also the death event
			self.S_pointer = self.add_item(self.S_pointer, time=k, 
				func=self.death)
			#####if queue is empty just add to curr_time and continue
		else:	
			info = {"Ts" : 0} #ts is to be determined
			self.queue.append({"Ts": 0, "arrival": self.curr_time})

		# determine the next birth event
		k = self.gen_arrival_time.exp() 
		self.IAT.append(k)
		k =  int(k * 100) + self.curr_time			

		self.S_pointer = self.add_item(self.S_pointer, time= k, func=self.birth) # at time s there is a new 


	def death(self):
		print("Death event has been called")

		k_first = int(self.gen_serivice_time.exp() * 100)
		self.service_times.append(k_first/100.0)

		self.departures += 1

		req = self.queue.pop(0) #remove first item in queue

		self.waiting_times.append( float(self.curr_time - req["arrival"]) / 100.0)
		#assign service time for the next, essentially assigning the next death event

		if not self.queue or isinstance(self.queue, int):
			print("Empty queue")
			self.queue_is_empty = True

			#self.print_cal(self.S_pointer)
			#print("INFOOOOO ::: ", self.S_pointer.time)
			"""
			if  self.S_pointer.next == None : # calander is empty and other items
				k =  int(np.random.exponential(1/self.Ts)) + self.curr_time			
				
				self.S_pointer = self.add_item(self.S_pointer, time= k, func=self.birth) # at time s there is a new
			"""
			

			#if the queue is empty after removing the only one just return	
		else: #other items waiting in queue

			self.queue_is_empty = False

			k = self.curr_time + k_first

			#self.all_times.append(k_first)
			self.queue[0]["Ts"] = k

			self.S_pointer = self.add_item(self.S_pointer, time= k, func= self.death)

			print("Other items still in queue")


	def monitoring(self):

		""" @Param:
			@Return: void, prints current time,
		""" 
		#lambda = number of total arrivals / currtime
		#number being serviced / departures

		print( bcolors.HEADER + "\n------ Monitoring Report ------" + bcolors.ENDC)

		print("Idle time: ", self.idleTime)

		Ts = np.mean(self.service_times)

		print("Ts :",  np.mean(self.service_times) )
		q = len(self.queue) + 1
		print("Q: ", q )

		#print("Utilization: " , 1 - (float(self.idleTime) / float(self.curr_time`) ))
		IAT = np.mean(self.IAT)

		print("Mean IAT: ", IAT)

		print("Tw: ", np.mean(self.waiting_times))

		print("W: " , len(self.queue))
		
		Tq = np.mean(self.waiting_times) + Ts
		print("Average service Time (Tq): ", Tq)

		print("Utilization: " ,  Ts * self.lmb )

		queue = [i for i in self.queue]
		print("Status of Queue: ", queue)
		#self.print_cal(self.S_pointer)
		#print("Average service Time (Ts): ", np.mean(Tw))

		print("Current Time: ", str(self.curr_time) )
		print( bcolors.HEADER + "------ End Monitoring Report ------\n"  + bcolors.ENDC)

	def start_simulation(self):

		self.initializeState() 
		self.curr_time = 0

		monitor_time = int(np.random.exponential(1 / self.Ts))
		
		#print(self.S_pointer.time)
		
		while self.curr_time < (self.max_time * 2):
			#self.print_cal(self.S_pointer)

			if(self.queue_is_empty):
				self.idleTime += 1

			if(self.S_pointer.time == self.curr_time):

				event = self.S_pointer.func
				self.curr_time += 1
				#call the appropriate event
				event()
				#get next job 
				self.S_pointer = self.S_pointer.next

			else:
				self.curr_time += 1			
			#print(self.curr_time)

			if monitor_time == 0:
				monitor_time = int(rand.randVar(1.0/ 30.0).exp())
			elif self.curr_time % monitor_time == 0: #and self.curr_time > self.max_time:

				self.monitoring()
				monitor_time = int(rand.randVar(1.0/ 30.0).exp())


if __name__ == '__main__':
	print("lets start!!")



	obj = Simulation(1000, 5, 0.15)

	#obj = Simulation(1000, 6, 0.15)

	#obj = Simulation(1000, 6, 0.20)
	obj.start_simulation()
