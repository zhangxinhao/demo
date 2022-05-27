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

    public Future<String> addTask(Callable<String> task) {
        return executor.submit(task);
    }

    public void begin() {
        init();
        List<Future<String>> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            list.add(addTask(new MyTask()));
        }
        int num = 0;
        for (Future<String> future : list) {
            num++;
            try {
                String str = future.get();
                System.out.println("num: " + num + " str: " + str);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (ExecutionException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) {
        Pool pool = new Pool();
        pool.begin();

    }

    public class MyTask implements Callable<String> {

        @Override
        public String call() {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
            System.out.println("ThreadName: "+Thread.currentThread().getName());
            return "aaa";
        }
    }
}
