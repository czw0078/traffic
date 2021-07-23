# Agent-based Modeling for Freeway Network Traffic and an Adversarial Example 

This is the souce code for the paper.

## Quick run

Run main python source code file in the Linux/Mac terminal 
```bash
python3 ./main.py
```
The average travel time will be given after running the code.

<details>
<summary>Expand to see the video</summary>

https://user-images.githubusercontent.com/21988239/126753107-41cb6961-0dd8-460e-9dc2-670f76ba1fe8.mov
</details>

## Set up demand and freeway network

In the file "profile.py", user can change the three parameters of origin node number (O), destination node number (D), and how many vehicles enters the network per 20 second during the simulation (N).
```python
def get_ODN(): # O D N
    return OD_per_20_second_wait_200(0, 5, 10)
```

Inside the function "prepare_patch_list" body, user can modify the traffic network by edit node and road that connects them. 
The "v_free" is the best speed determined by the condition of the road, default 25 (135 km/h), and 11 (60 km/h) for slow road. 

## An adversarial example

Sometimes build more roads not always reduce the total travel time and may cause traffic congestion. 
Assume the vehicles are traveling from n0 to n5, some road with 135 km/h speed limit and some only 60 km/h.
In this example, build a single-way lane from n3 to n7 do not speed up the total traffic flow.
On the contracy, it slow 10 more second because every vehicle try to take short cut and it becomes more congested.
```
n0       n2     n4
   \  //   \\ /   \
    ||      n3     |
    n1             n5
     |     n7      |
     \    /  \\    //
       n6       n8
``` 

Uncomment the following line in "profile.py", a single way road from n3 to n7 will be set up
```python
# r9 = obj.road(n3, n7)
```

<details>
<summary>Expand to see the video</summary>

https://user-images.githubusercontent.com/21988239/126753147-6a199976-09da-48af-8c6e-e230fa2c2f2f.mov
</details>

