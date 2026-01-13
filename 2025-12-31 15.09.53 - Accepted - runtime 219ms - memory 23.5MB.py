class Solution:
    def findCrossingTime(self, n: int, k: int, time: List[List[int]]) -> int:
        import heapq
        
        # time[i] = [leftToRight, pickOld, rightToLeft, putNew]
        # efficiency = leftToRight + rightToLeft (higher = less efficient)
        # Less efficient workers have priority for bridge
        
        # Priority queues: (-efficiency, -index) for waiting
        # (availableTime, efficiency, index) for working
        
        leftWait = []   # Workers waiting on left side, max heap by (-efficiency, -index)
        rightWait = []  # Workers waiting on right side, max heap
        leftWork = []   # Workers working on left (putting boxes), min heap by time
        rightWork = []  # Workers working on right (picking boxes), min heap by time
        
        # Initially all workers wait on left
        for i in range(k):
            eff = time[i][0] + time[i][2]
            heapq.heappush(leftWait, (-eff, -i))
        
        currentTime = 0
        boxesRemaining = n
        
        while boxesRemaining > 0 or rightWork or rightWait:
            # Move workers who finished working to waiting queues
            while leftWork and leftWork[0][0] <= currentTime:
                _, eff, i = heapq.heappop(leftWork)
                heapq.heappush(leftWait, (-eff, -i))
            
            while rightWork and rightWork[0][0] <= currentTime:
                _, eff, i = heapq.heappop(rightWork)
                heapq.heappush(rightWait, (-eff, -i))
            
            # Right side has priority (workers returning with boxes)
            if rightWait:
                _, negI = heapq.heappop(rightWait)
                i = -negI
                # Cross bridge right to left
                crossTime = time[i][2]
                currentTime += crossTime
                # After crossing, put box (work on left side)
                putTime = time[i][3]
                eff = time[i][0] + time[i][2]
                heapq.heappush(leftWork, (currentTime + putTime, eff, i))
            elif leftWait and boxesRemaining > 0:
                _, negI = heapq.heappop(leftWait)
                i = -negI
                # Cross bridge left to right
                crossTime = time[i][0]
                currentTime += crossTime
                # After crossing, pick box (work on right side)
                pickTime = time[i][1]
                eff = time[i][0] + time[i][2]
                heapq.heappush(rightWork, (currentTime + pickTime, eff, i))
                boxesRemaining -= 1
            else:
                # No one can use bridge, advance time
                nextTime = float('inf')
                if leftWork and boxesRemaining > 0:
                    nextTime = min(nextTime, leftWork[0][0])
                if rightWork:
                    nextTime = min(nextTime, rightWork[0][0])
                if nextTime == float('inf'):
                    break
                currentTime = nextTime
        
        return currentTime