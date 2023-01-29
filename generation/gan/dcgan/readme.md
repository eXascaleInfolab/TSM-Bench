## Data Generate

#### Introduction

The main function of this module is to simulate and generate credible time series data.
In order to simulate time series more effectively and generate time series more effectively, we propose a massive time series data generation framework, which has the following steps:
Creating seed fragments (sequences) based on real-time sequence data usually limits the data size.

- Use certain generative adversarial network (GAN) models to generate synthetic fragments from real seeds.
- Create a directed graph of synthesized fragments.
- On the directed graph of the synthesized segment. Use random walk algorithm to generate continuous time series

#### Start

1. first train DCGAN model ``python DCGAN.py``

2. then train the encoder model ``python encoder_dc.py``

3. execute benchmark  ``python test_dc.py``
