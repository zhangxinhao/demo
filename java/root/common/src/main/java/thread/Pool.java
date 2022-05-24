package thread;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class Pool {
    private ExecutorService executor;

    private final int CORE_POOL_SIZE = 2;
    private final int MAX_POOL_SIZE = CORE_POOL_SIZE * 2;
    private final int KEEP_ALIVE_HOURS = 1;

    public void init() {
        executor = new ThreadPoolExecutor(CORE_POOL_SIZE, MAX_POOL_SIZE, KEEP_ALIVE_HOURS, TimeUnit.HOURS, new LinkedBlockingDeque<>(100));
    }

    public void addTask(Runnable task) {
        executor.execute(task);
    }

    public void begin() {
        init();
        for (int i = 0; i < 10; i++) {
            addTask(new MyTask());
        }
    }

    public static void main(String[] args) {
        Pool pool = new Pool();
        pool.begin();

    }

    public class MyTask implements Runnable {

        @Override
        public void run() {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
            System.out.println("ThreadName: "+Thread.currentThread().getName());
        }
    }
}
