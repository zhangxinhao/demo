package thread;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class Pool {
    private ExecutorService executor;

    private final int CORE_POOL_SIZE = 2;
    private final int MAX_POOL_SIZE = CORE_POOL_SIZE * 2;
    private final int KEEP_ALIVE_HOURS = 1;

    public void init() {
        executor = new ThreadPoolExecutor(CORE_POOL_SIZE, MAX_POOL_SIZE, KEEP_ALIVE_HOURS, TimeUnit.HOURS, new LinkedBlockingDeque<>(100));
    }

    public Future<?> addTask(Runnable task) {
        return executor.submit(task);
    }

    public void begin() {
        init();
        List<Future> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            list.add(addTask(new MyTask()));
        }
        int num = 0;
        for (Future future : list) {
            num++;
            try {
                future.get();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (ExecutionException e) {
                throw new RuntimeException(e);
            }
            System.out.println("num: " + num);
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
