# Unraveling the Magic of Amplifiers

Amplifiers are critical components in amateur radio, enhancing the strength of signals and making long-distance communication possible. As a radio operator, understanding their functioning and different types will help you get the best out of your radio station. In this chapter, we delve into the various classes of operation, the difference between vacuum tube and solid-state circuits, distortion and intermodulation, spurious and parasitic suppression, and the concept of switching-type amplifiers.

## Amplifier Classes and Their Significance

Amplifiers can be categorized into different classes—A, AB, B, C, and D—based on the portion of the input signal cycle during which the amplifier is active. 

A **Class A amplifier** operates during the entire input signal cycle. Its operating point, in a common emitter configuration, is approximately halfway between saturation and cutoff. This class of amplifiers is known for excellent linearity and low distortion but is the least efficient.

**Class AB amplifiers**, such as a push-pull amplifier, operate for more than 180 degrees but less than 360 degrees of the input signal cycle. These amplifiers are a compromise between Class A and Class B amplifiers, providing a good balance between efficiency and linearity.

**Class B amplifiers** are active for exactly 180 degrees of the input signal cycle. These amplifiers are more efficient than Class A amplifiers but suffer from a distortion known as crossover distortion.

**Class C amplifiers** are even more efficient, but they operate for less than 180 degrees of the input signal cycle. They are typically used in applications where distortion is less critical, such as signal transmission. When used to amplify a single-sideband phone signal, however, a Class C amplifier can lead to signal distortion and excessive bandwidth.

**Class D amplifiers** are different from the rest. Instead of linear amplification, they use switching technology to achieve high efficiency. The active device in a Class D amplifier is either fully on (saturated) or fully off (cutoff), reducing power losses and making these amplifiers more efficient than linear amplifiers.

## Amplifier Circuits and Components

An amplifier circuit can take different configurations, each with unique characteristics. 

A **common emitter amplifier**, for instance, is characterized by an operating point approximately halfway between saturation and cutoff. This is the most widely used amplifier configuration due to its high voltage and power gain.

On the other hand, an **emitter follower (or common collector) amplifier** is known for its high input impedance, low output impedance, and unity gain. The input and output signals of an emitter follower are in-phase, making it ideal for impedance-matching applications.

A **grounded-grid amplifier** is another type of amplifier circuit commonly used in radio-frequency applications. One of its key characteristics is low input impedance.

In amplifier circuits, resistors play crucial roles. For instance, in the amplifier circuit shown in Figure E7-1, resistors R1 and R2 serve as a voltage divider for biasing, while R3 acts as an emitter bypass resistor. This arrangement is part of the self-biasing system of the amplifier.

## Keeping Amplifier Performance in Check

While amplifiers are necessary for enhancing signal strength, they can also introduce unwanted effects such as distortion and oscillations. To prevent these issues, certain measures can be taken.

For instance, to prevent unwanted oscillations in an RF power amplifier, one can install **parasitic suppressors** or neutralize the stage. Parasitic suppressors help eliminate unwanted parasitic oscillations that can cause instability and even damage to the amplifier. Neutralizing the stage involves introducing a phase shift to cancel out the undesired feedback that leads to oscillations.

Another important aspect of amplifier performance is the suppression of spurious and parasitic elements. The output of an RF switching amplifier, for example, requires a filter to remove harmonic content and ensure the purity of the output signal.