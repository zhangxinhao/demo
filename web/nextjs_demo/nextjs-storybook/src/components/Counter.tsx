'use client'

import { useCounterStore } from '@/store/counterStore'

export function Counter() {
  const { count, increment, decrement, reset } = useCounterStore()

  return (
    <div className="flex flex-col items-center gap-4 p-6 rounded-lg bg-gray-100 dark:bg-gray-800">
      <h2 className="text-2xl font-bold">Count: {count}</h2>
      <div className="flex gap-2">
        <button
          onClick={decrement}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
        >
          -1
        </button>
        <button
          onClick={reset}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition"
        >
          Reset
        </button>
        <button
          onClick={increment}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
        >
          +1
        </button>
      </div>
    </div>
  )
}

