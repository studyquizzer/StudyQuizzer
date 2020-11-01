import os
import time
import signal
import socket

from threading import Thread, currentThread
from multiprocessing import Process, Event, Semaphore, Value, cpu_count


class PooledProcessMixIn:
    """
    A Mix-in added by inheritance to any Socket Server like BaseHTTPServer to provide concurrency through
    A Pool of forked processes each having a pool of threads
    """

    def _handle_request_noblock(self):
        """
        Handle one request without blocking
        """
        if not getattr(self, "_pool_initialized", False):
            self._init_pool()
        self._event.clear()
        self._semaphore.release()
        self._event.wait()

    # ------------------------------------------------------------------------------------------------------------------

    def _real_handle_request_noblock(self):
        """
        Real handle request
        """
        try:
            # TODO: timeout
            request, client_address = self.get_request()
        except socket.error:
            self._event.set()
            return
        self._event.set()
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
                self.shutdown_request(request)
            except Exception:
                self.handle_error(request, client_address)
                self.shutdown_request(request)

    def _init_pool(self):

        self._pool_initialized = True
        self._process_n = getattr(self, "_process_n", max(2, cpu_count()))
        self._thread_n = getattr(self, "_thread_n", 64)
        self._daemon = getattr(self, "_daemon", False)
        self._kill = getattr(self, "_kill", True)
        self._debug = getattr(self, "_debug", False)
        self._logger = getattr(self, "_logger", None)
        self._keep_running = Value("i", 1)
        self._shutdown_event = Event()
        self._shutdown_event.clear()
        self._event = Event()
        self._semaphore = Semaphore(1)
        self._semaphore.acquire()
        self._closed = False
        self._maintain_pool()

    def _maintain_pool(self):
        """
        Fork processes
        """
        self._processes = []
        for _ in range(self._process_n):
            t = Process(target=self._process_loop)
            t.start()
            self._processes.append(t)

    def _process_loop(self):
        """
        Start threads
        """
        threads = []
        for _ in range(self._thread_n):
            t = Thread(target=self._thread_loop)
            t.setDaemon(self._daemon)
            t.start()
            threads.append(t)
            if self._logger:
                self._logger.debug("%s started" % t.name)
        self._shutdown_event.wait()
        if self._logger:
            self._logger.debug("process terminated")
        for t in threads:
            t.join()

    def _thread_loop(self):
        """
        Thread loop
        """
        while self._keep_running.value:
            self._semaphore.acquire()
            if self._keep_running.value:
                self._real_handle_request_noblock()
        if self._logger:
            self._logger.debug("%s terminated" % currentThread().name)

    def pool_shutdown(self):
        """
        Pool shutdown
        """
        self._keep_running.value = 0
        for _ in range(self._process_n * self._thread_n):
            self._semaphore.release()
        self._shutdown_event.set()

    def shutdown(self):
        """
        Server shutdown
        """
        self.pool_shutdown()
        time.sleep(1)
        for p in self._processes:
            p.terminate()
        self._closed = True
        if self._kill:
            os.kill(os.getppid(), signal.SIGTERM)

    @property
    def closed(self):
        """
        Pool status
        :return: True if pool closed
        """
        return self._closed
