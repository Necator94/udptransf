# UDP transfering of files
-----------------------------------------------------------------------------------------------------------------------------
UDP client/server with guaranteed delivery of packets (implemented on python)

Some features of sockets:

| Latency, s | Loss, % | Required time, s | Real transfering time, s |
|------------|---------|------------------|--------------------------|
| 0          | 0       | Less than 10     | 0.39                     |
| 10         | 1       | Less than 12     | 2.42                     |
| 10         | 10      | Less than 14     | 3.03                     |
| 100        | 10      | Less than 20     | 13.44                    |
| 1000       | 1       | Less than 40     | 21.7                     |
