import json, time # json.dumps() time.monotonic()
from collections import OrderedDict #d.popitem(last=False) d.move_to_end | [key]In input order
from dataclasses import dataclass, field #field(default_factory=lambda: defaultdict(Counter))
from dataclasses import asdict #asdict(class with @dataclass)
from enum import IntFlag, auto  # | &= ~
from functools import lru_cache # @lrucache(maxsize=128)
from functools import cached_property
from threading import Lock, RLock #Lock RLock threading.Thread(target= ,args=) start
from threading import Condition # c=threading.Condition() with c c.wait() c.wait_for() c.notify() c.notify_all()
from threading import Semaphore # sem = threading.Semaphore() with sem
from collections import defaultdict #defaultdict[Callable Call When no item] lambda: defaultdict[Counter]
from contextlib import contextmanager # def.. yield
from contextlib import suppress # with surpress(..)
from itertools import islice # batch:= list(islice(it, 2))
from itertools import count  #count() next(count())  iter([1, 2])
from concurrent.futures import ThreadPoolExecutor #with TPE(max_workers=4) as ec: f=ec.submit(a,1) f.done() f.result()
from concurrent.futures import as_completed #for f in as_completed(futures_devices) futures_devices[f] = dev
import subprocess # res=run(['ls', '-l']) (res.returncode stdout stderr) | process=Popen pid terminate wait poll
from abc import ABC, abstractmethod   # ABC @abstractmethod
import asyncio # async def | asyncio.create_task(a(1)) asyncio..run(b(2)) | t.cancel() t.as_completed() | await t
from typing import ParamSpec, TypeVar, Callable # P = ParamSpec("P") R = TypeVar("R") Callable[[str], int]
import logging #getLogger basicConfig(level=logging.INFO,)

# , Empty, Full
from collections import Counter #Counter()["abc"] += 1 most_common
from threading import Event     # e=threading.Event() e.set() e.clear() e.is_set() e.wait()
from queue import Queue, \
    Empty, \
    Full  # a=Queue(maxsize=5) a.put("k")  a.get(timeout=1) a.task_done()++ a.join()   size New: Block until get!!
from collections import deque  # a=deque(maxlen=4)  a.append(1) a.popleft()    len  New: Delete Old!!!!!!!
import heapq                   # jobs = [] heappush(jobs, (-3,"a")) heappop() | heapq.heapify(some_list)


import threading
logger = logging.getLogger(__name__) # DEBUG INFO WARNING ERROR CRITICAL
logging.basicConfig(
    level=logging.INFO,
)
P = ParamSpec("P") #Signature -> (host: str, port: int, timeout:float = 5_
R = TypeVar("R")   #Type -> str/int/Device
def check_call(call_func: Callable[[str], int]) -> int:
    return call_func("Hello")
assert check_call(lambda x: len(x)) == 5

async def worker(name, delay):
    print(name, "start")
    time.sleep(delay)
    print(name, "done")
    return 2
async def main():
    tasks = [
        asyncio.create_task(worker("A", 2)),
        asyncio.create_task(worker("B", 1)),
        asyncio.create_task(worker("C", 3)),
    ]
    async with asyncio.timeout(5):
        result_a = await tasks[0]
    tasks[1].cancel()
    for task in asyncio.as_completed(tasks):
        try:
            result = await task
        except asyncio.CancelledError:
            print("cancelled")
        except Exception:
            logger.exception("job failed")

        print(result)

asyncio.run(main())

jobs = []
sequence = count()
heapq.heappush(jobs, (-10, next(sequence), "critcal"))
heapq.heappush(jobs, (-4, next(sequence), "normal"))
heapq.heappush(jobs, (-7, next(sequence), "high"))
heapq.heappop(jobs)
priority_number, priority_name = heapq.heappop(jobs)
some_list =[7, 4, 2]
heapq.heapify(some_list)
heapq.heappop(some_list)

# TypeError for not implementing run_job
class Target(ABC):

    @abstractmethod
    def run_job(self, job):
        pass

class RemoteTarget(Target):

    def run_job(self, job):
        super().run_job(job)

# process  = subprocess.Popen
# process.pid
# process.poll()
# process.terminate()
# process.wait()
result = subprocess.run(
    ["ping", "-c", "3", "10.0.0.1"],
    input="Hello",
    capture_output=True, # out to result.stdout
    text=True, # לתרגם אוטומטית את הטקסט כי זה נתפס כביטים
    check=True, # To throw subProcessError on error
    timeout=3,
)
# stdin = Input
a = result.returncode # Worked -> 0
b = result.stdout
c = result.stderr

def check_device(device):
    print("Device is fine")
    return 123
devices = ["nic-1", "nic-2", "nic-3", "nic-4"]
future_to_device = {}   # defaultdict("Callable Call When no item for the value")

with ThreadPoolExecutor(max_workers=4) as executor:
    for dev in devices:
        future = executor.submit(check_device, dev)
        future.done()
        future.exception() # return exception or None if no exception occured
        # החיפוש הוא על המפתחות ולכן המפתחות צריכות להיות ה-future!!
        future_to_device[future] = dev  # ה-Future הוא המפתח!

if future_to_device[0].done():
    print("Work of first device in list ended already!")

# החיפוש הוא על המפתחות ולכן המפתחות צריכות להיות ה-future!!
for f in as_completed(future_to_device):
    device = future_to_device[f] # שליפת המכשיר לפי ה-Future שסיים כרגע
    try:
        result = f.result()
    except Exception as ex:
        print(f"{device} test failed: {ex}")
    else:
        print(f"{device} test result: {result}")

#StopIteration עבור רשימות שהסתיימו
my_list = [1, 2]
it = iter(my_list)
next(it)
next(it)
with suppress(StopIteration):
    next(it)

counter = count(start=5)
next(counter)

devices_example = [
    ("nic-1", "PASS"),
    ("nic-4", "FAIL"),
    ("nic-2", "PASS"),
    ("nic-4", "PASS"),
]
# print(devices_example)
print(sorted(devices_example, key=lambda x: x[0])) # מחזיר רשימה ממוינת חדשה ולא נוגע בקודמת
# print(devices_example.sort(key=lambda x: x[0])) # לא מחזיר ערך וממיין את הרשימה המקורית
# print(devices_example)

it11 = iter([1, 2, 3, 4, 5, 6, 7])
size = 3
while batch:=list(islice(it11,size)):
    print(batch)
batch = list(islice("file: text text text tex", 1000))
it = iter([1, 2,3 ,4, 5])
chunk = list(islice(it, 2))
print(chunk)
islice(it, 2)
print(list(islice(it,2)))

with suppress(ConnectionError, ValueError):
    raise ValueError("aaaa")

print("HI")

@contextmanager
def enter_and_exit():
    a = 0
    print("Hello there let's start")
    try:
        yield a
    finally:
        a += 1
        print("Well I guess we're done")

try:
    with enter_and_exit():
        raise ValueError("123")
        # print("Do some work")
except ConnectionError:
    print("It's ok lets move on")

counts = Counter()
counts["error-1"] += 1
counts.most_common(1)
counts.update(['error-1', 'error8'])
counts.subtract(['error-2', 'error9'])
counts = +counts

for key in counts:
    counts[key] -= 1

some_counter_dict = defaultdict(Counter)


class DevicesLog:
    devices_err_counter : defaultdict[str, Counter] = field(default_factory=lambda: defaultdict(Counter))

time_start= time.monotonic()
deadline= time.monotonic() + 5


jobs = Queue(maxsize=5)
jobs.put("job-1")
jobs.put("job-2", timeout=0.1)
jobs.put("job-3", block=False) # אם עדין מלא מחזיר queue.Full
jobs.put_nowait("job-4") # אם עדין מלא מחזיר queue.Full
jobs.put_nowait("job-5") # אם עדין מלא מחזיר queue.Full
jobs.get() # FIFO + Sleep until jobs.put

# ValueError: task_done() called too many times עבור יותר מדי משימות שסוימו
jobs.task_done() # אומר שעבודה כלשהי סוימה ועובד כקאונטר
jobs.join() # יכה שכולם יסומנו כסוימו

try:
    jobs.put_nowait("job-6") # אם עדין מלא מחזיר queue.Full
except Full:
    print("Queue is full")

jobs.get() # FIFO + Sleep until jobs.put
jobs.get(timeout=0.1) # When time out return queue.Empty
jobs.get_nowait() # timeout is zero
jobs.get(block=False) # Same as jobs.get_nowait()

try:
    jobs.get(timeout=0.1)
except Empty:
    print("No item arrived")

def do_work():
    print("Doing some work..")

semaphore = threading.Semaphore(3) # עד 3 תרדים במקביל ואם נוצרים עוד אז הם מחכים שהיגמרו חלק מהנוכחיים
with semaphore: # semaphore.acquire() -> try run -> semaphore.release()
    do_work()


stop_event = threading.Event()
stop_event.set()
stop_event.clear()
stop_event.wait()
stop_event.wait(timeout=0.1)
stop_event.is_set()

jobs = deque()
condition = threading.Condition()
condition.wait()
condition.wait(timeout=0.1)
condition.wait_for(lambda: bool(jobs))
condition.notify()
condition.notify_all()

class JobsControl:
    def __init__(self):
        self.jobs = deque()

    def do_work(self):
        # condition_with_lock = threading.Condition(threading.Lock) # אפשר לתת לוק משלנו
        with condition: # condition.acquire() -> try run -> condition.release()
            print("check for jobs")
            # condition.wait_for(lambda: bool(jobs), timeout=5)
            condition.wait_for(lambda: bool(self.jobs))
            job = self.jobs.pop()

# RLock חשוב אם מספר מתודות בתור האינסטנס כן יכולות לרוץ באותו זמן
class Example:
    def __init__(self):
        self._lock = threading.RLock()
        self.balance_a = 50
        self.balance_b = 90

    def operation_a(self):
        with self._lock:
            self.balance_a +=5

    def operation_b(self):
        with self._lock:
            self.balance_b +=5


lock = threading.Lock()
balance = 15
with lock: # -> lock.aquire + try run + finally lock.release()
    balance +=10

def expensive_parse():
    print("Very long parse")
class Device:
    def __init__(self, raw_config):
        self.raw_config = raw_config

    # הערך שעליו מסתמך יכול להשתנות ועדין יחזיר אותה תוצאה!! מסוכן
    @cached_property
    def parse_config(self):
        print("parsing")
        return expensive_parse(self.raw_config)

    def clear_cache_parse_config(self):
        if "parse_config" in self.__dict__:
            del self.__dict__["parse_config"]

# @lru_cache(maxsize=None)
@lru_cache(maxsize=128)
def call_me_hunder_is_same_as_one(x):
    return x+2
call_me_hunder_is_same_as_one(2)


def default_friends():
    return ["ChatGPT", "Claude", "ImaginaryBob"]

class DevicesNames(IntFlag):
    NIC = auto()
    RDMA = auto()
    CRYPTO = auto()
caps = DevicesNames.NIC | DevicesNames.RDMA | DevicesNames.CRYPTO
required = DevicesNames.RDMA | DevicesNames.CRYPTO
# caps &= ~Devices.RDMA
if ( caps & required ) == required:
    print("Device have all required")


@dataclass
class UserDetails:
    name: str
    friends: list[str] = field(default_factory=default_friends)

user_bill = UserDetails("Bill")
dict_bill = asdict(user_bill)
print(dict_bill)
print(json.dumps(dict_bill))
d = OrderedDict()
d["A"] = 1
d["B"] = 2
d["C"] = 3
d.move_to_end("A")
print(d)


d["D"] = 3
d.popitem(last=False) # נניח מותר רק 3 איברים
print(d)

q = deque(maxlen=4)
q.append(1)
q.append(2)
q.append(3)
q.append(4)
q.append(5)
a = q.popleft()
# print(a)
# print(q)

def hello():
    print("Hello World")