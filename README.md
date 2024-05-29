As part of my EV conversion project I wanted to get a better grip on how an electric motor would perform against an ICE powered car. Lots of people have commented on how any Seven with an electric motor will probably be a crazy accelerating beast. But while that could be the case, the amount of space in a Seven chassis (even an SV) may be prohibitive.

And what matters is torque at the wheels. As we all know "power" is just torque multiplied by RPM. So its torque that determines the performance of your vehicle.

Then you have to take into account any gearing between the motor and wheels. Any gear reduction will "amplify" the torque created at the output (and gearing up will decrease output torque of course).

But in general a Seven has a gearbox going one stage of gear reduction followed by a differential doing a second stage. And then the differential also splits the torque in two to each wheel.

Therefore, the torque to each rear driven wheel at any given motor speed is: 

  wheel_torque = motor_torque * gearbox_ratio * differential_ratio / 2.

So it should be simple to come up with a Wheel Torque vs Speed graph, showing the torque produced by the motor.

I tried to come up with a way of doing this in a spreadsheet but found it was a bit of a blunt instrument. So, I wrote a script.

I made the script so it can be reasonably easily modified to provide different "motors" and "gearboxes". The script runs through each motor configuration and plots each gear it finds in the gearbox on a chart. 

THIS CODE IS NOT PRODUCTION GRADE: I threw this together for my own benefit. If I'd have wanted to get paid for the code then it would have looked quite different. It also evolved and could probably do with a refactor and prune.

Anyway, here's a plot form the code as it stands at posting date. I created a benchmark set of in-gear plots for a Caterham Seven 420 (I found the data at the link repeated in the code). I then created two motor variants based around a motor I'm thinking of using in my conversion project. The two variants vary by the current that can be supplied to the motor and by a gear reduction I'll need to include in the design.

![Sample Graph](https://github.com/Purplemeanie/TorqueAndPowerComparisons/raw/main/SPX177%20Wheel%20Torque%20Comparisons.png "Simple Graph")

You can see from the graph that for the variants I've configured, the 420 beats the EV configurations in 1st gear but the EVs then take the lead from 2nd gear onwards.
