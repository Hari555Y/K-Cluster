# K-Clustering

In this project we are working on a very interesting project related to k-clustering algorithm. For any generic case we have assumed that there are two types of population/parameters (n1 and n2) which are scattered uniformly in an area. Now, we initially formed k centers/facilities which are available for both the populations and then we tried to minimize the sum of squares of distance of the nearest facility for all the people. This way we have trained our algorithm. Now as any general case we have assumed that one of the population has underreported its parameter given. This will now have some direct implications on both the populations.
Firstly, we have taken the number of facilities as a function of total population (both the n1 and n2 parameter populations).
As the underreported population has less people we know that their influence (sum of squares distance) will have less hold now and thus the facilities are shifted towrds the other population more. So, now this population (underreported one) will have to move more to reach the nearest facility. Thus we are calling it unprivileged.
On the contrary, the other one will be privileged one and have some benefits of the other population underreporting.
After that we draw the plots of all these (total cost, privileged cost, unprivileged cost) and saw their variations are kind of linear in small percentage of underreporting.

Also, we have implemented various other algorithms of the same form (Alternate square , scaling the total square size, taking n as constant density and then choosing different number of squares of the two populations) so as to insure that randomization has no effect on the graphs and deductions we have obtained. 

Now, we have discussed some ways to tackle this problem :
We fix that any facility have only this much percent population of the first density here.
On the other hand we can also limit the distance such that any facility cannot be very much close to the normal (n2) density population in all nearby squares.

This way we will be finding/generalising our algorithm to take care of underreporting by a population and give best results (both populations treated equally) independent of all values. 
