# Unraveling the Intricacies of Feed Lines and Standing Wave Ratios

In this section, we will delve deep into the world of feed lines and standing wave ratios (SWR). We will unravel the factors that determine the characteristic impedance of a parallel conductor feed line, the relationship between high SWR and transmission line loss, and the nominal characteristic impedance of “window line” transmission line. We will also explore what causes reflected power at an antenna’s feed point, how the attenuation of coaxial cable changes with increasing frequency, and in what units RF feed line loss is usually expressed. 

## Understanding Characteristic Impedance

Characteristic impedance is an important aspect of feed lines. It is determined by the distance between the centers of the conductors and the radius of the conductors. This is a crucial element to consider when designing or evaluating the efficiency of a feed line.

"Window line" transmission lines have a nominal characteristic impedance of 450 ohms. This characteristic impedance is very specific to window lines and different types of transmission lines will have different characteristic impedances.

## The Impact of Standing Wave Ratio (SWR) 

The standing wave ratio (SWR) is a measure of the efficiency of the energy transmission along a feed line. A high SWR is indicative of an inefficient transmission line where a significant amount of the energy is being reflected back towards the source instead of being absorbed by the load (the antenna). 

In relation to transmission line loss, a high SWR increases loss in a lossy transmission line. This is because the reflected power is absorbed by the line, increasing its temperature and thus its resistance, which in turn causes more power loss.

## Reflective Power and Feed Line Attenuation

Reflected power at an antenna’s feed point is generally due to a difference between feed line impedance and antenna feed point impedance. This mismatch leads to power being reflected back from the antenna towards the transmitter, decreasing the efficiency of power transfer.

As for feed line attenuation, it increases with increasing frequency. This is primarily due to the skin effect where the AC signal tends to concentrate towards the surface of the conductor, effectively reducing the cross-sectional area of the conductor and thus increasing its resistance.

## Measuring Feed Line Loss

Feed line loss is usually expressed in decibels per 100 feet. It's important to note that feed line loss is not just dependent on the length of the cable, but also on the frequency of operation and the properties of the cable itself.

## Mitigating Standing Waves on a Feed Line

To prevent standing waves on a feed line connected to an antenna, the antenna feed point impedance must be matched to the characteristic impedance of the feed line. This allows for maximum power transfer and minimum reflection.

## SWR Impact on Feed Line

When a matching network is used at the transmitter end of a feed line to present a 1:1 SWR to the transmitter, the SWR on the feed line remains 5:1. This is because the SWR on the line is defined by the load (the antenna) and the line itself, and the matching network does not change either of these factors.

## SWR Resulting from Different Load Impedances

When a 50-ohm feed line is connected to a 200-ohm resistive load, the resulting SWR is 4:1. Similarly, when a 50-ohm feed line is connected to a 10-ohm resistive load, the resulting SWR is 5:1. These values are calculated by dividing the load impedance by the line impedance (or vice versa if the load impedance is lower than the line impedance).

## Transmission Line Loss and SWR

Finally, transmission line loss affects the SWR measured at the input to the line. Higher loss reduces SWR measured at the input to the line. This is because the lossy line absorbs a part of the reflected power, which decreases the reflected power at the input, and hence decreases the SWR.