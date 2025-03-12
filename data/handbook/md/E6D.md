# The Intricacies of Inductors, Transformers and Piezoelectricity

In this section, we'll delve into the fascinating world of inductors, transformers, and piezoelectricity. These are integral components in the realm of electronics and understanding them will enhance your proficiency in amateur radio.

## Discovering Piezoelectricity

**Piezoelectricity** is a characteristic of certain materials that generate a voltage when mechanically stressed, and conversely, flex or deform when a voltage is applied. These materials possess the unique ability to convert mechanical energy into electrical energy and vice versa. This property is utilized in a wide range of practical applications, including microphones, sensors, and piezoelectric crystals used in quartz watches.

A **quartz crystal**, for example, can be modeled as a series RLC circuit in parallel with a shunt capacitance. The shunt capacitance represents the electrode and stray capacitance within the crystal. Understanding this equivalent circuit is crucial to manipulating the resonant frequency of a crystal oscillator circuit, which is commonly used in frequency control applications.

## Exploring Inductors and Transformers

Let's now shift our focus to inductors and transformers. In an inductor, the core material property that determines the inductance is **permeability**. A core with higher permeability will yield a higher inductance.

Inductors and transformers often have cores constructed of thin layers. This design choice is not to simplify manufacturing or reduce costs, but rather to reduce power loss caused by **eddy currents**. Eddy currents are circulating currents induced within the core by the changing magnetic field. By using thin, insulated layers, these currents are minimized, leading to more efficient operation.

## Core Material Considerations

The core material used in an inductor can greatly affect its characteristics. For instance, **ferrite** and **powdered iron** are commonly used core materials. While ferrite cores generally have lower initial permeability, they offer better temperature stability compared to powdered iron.

A **toroidal core** is a specific type of core used in inductors and transformers. The primary advantage of using a toroidal core over a solenoidal core lies in its ability to confine most of the magnetic field within the core material, reducing electromagnetic interference.

The choice of core material also plays a role in the behavior of an inductor under high magnetic flux conditions. **Inductor saturation** occurs when the core material can no longer increase its magnetization with an increase in applied magnetic field. This is typically caused by operation at excessive magnetic flux.

## The Role of Transformers

Transformers are devices that transfer electrical energy between two or more circuits through electromagnetic induction. When there is no load on the secondary winding of a transformer, a small amount of current, known as the **excitation current**, flows in the primary winding. This current is necessary to magnetize the core of the transformer.

## Suppressing Parasitics with Ferrite Beads

Finally, let's touch on the subject of parasitic suppression. In high frequency applications, such as VHF and UHF transistor amplifiers, **ferrite beads** are commonly used as parasitic suppressors at the input and output terminals. These simple yet effective components act as impedance elements that absorb high-frequency noise, preventing it from interfering with the desired signals.