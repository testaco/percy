# Mastering Receiver Performance Characteristics

Receiver performance characteristics are fundamental to the operation of any radio system. In this section, we'll delve into some of the critical concepts, including dynamic range, intermodulation and cross-modulation interference, third-order intercept, desensitization, preselector, sensitivity, and link margin. Understanding these concepts will allow you to optimize your radio operations and troubleshoot potential issues effectively.

## The Dynamics of Receiver Range

The **dynamic range** of a receiver is a key characteristic that determines its performance under different signal conditions. The dynamic range is defined as the difference between the receiver's noise floor (the lowest signal level the receiver can detect) and the maximum signal level it can handle without distortion.

**Blocking dynamic range** is a specific characteristic of a receiver, describing the difference in dB between the noise floor and the level of an incoming signal that will cause 1 dB of gain compression. This means that a receiver with a large blocking dynamic range can handle a wider range of signal levels without experiencing distortion.

However, a receiver with poor dynamic range can experience problems, including spurious signals caused by cross modulation and desensitization from strong adjacent signals. Cross modulation occurs when a strong signal modulates another signal, causing unwanted spurious signals. Desensitization is a reduction in receiver sensitivity caused by a strong signal near the received frequency.

## Intermodulation Interference

**Intermodulation interference** is a form of signal distortion that can occur when two or more signals mix in a nonlinear system, such as a radio receiver or transmitter. This mixing can produce new frequencies that are the sum and difference of the original frequencies and their harmonics. Intermodulation can create interference between two repeaters in close proximity when the output signals mix in the final amplifier of one or both transmitters.

To reduce or eliminate intermodulation interference in a repeater caused by a nearby transmitter, a band-pass filter can be used in the feed line between the transmitter and receiver. This filter allows only the desired frequency range to pass, reducing the potential for intermodulation interference.

## Receiver Desensitization and Preselectors

As previously mentioned, **desensitization** is a reduction in receiver sensitivity caused by a strong signal near the received frequency. One way to reduce the likelihood of receiver desensitization is to insert attenuation before the first RF stage, which can help to prevent strong signals from overloading the receiver.

A **preselector** is a type of filter used in a communications receiver to increase the rejection of signals outside the band being received. By limiting the range of frequencies that reach the RF amplifier, a preselector can help to prevent overloading and reduce the likelihood of intermodulation interference.

## Third-order Intercept and Intermodulation Products

The **third-order intercept (IP3)** is a theoretical point on a receiver's response curve where the power of a third-order intermodulation product equals the power of the input signals. In practical terms, a higher third-order intercept point indicates a receiver with better linearity and immunity to intermodulation distortion.

Intermodulation products are the sum and difference frequencies produced when two or more signals mix in a nonlinear system. Odd-order intermodulation products are of particular interest because they tend to fall within the band being received, potentially causing interference.

## Sensitivity and Link Margin

**Sensitivity** is a measure of a receiver's ability to detect weak signals. It is typically defined as the minimum discernible signal (MDS), which is the lowest signal level that the receiver can detect.

**Link margin** is a measure of the excess signal level available in a radio link, above the minimum required for reliable communication. It is calculated by considering factors such as transmit power, antenna gain, cable loss, path loss, receiver sensitivity, and required signal-to-noise ratio. A positive link margin indicates that the signal level is sufficient for reliable communication, while a negative link margin suggests that the signal level is too low.