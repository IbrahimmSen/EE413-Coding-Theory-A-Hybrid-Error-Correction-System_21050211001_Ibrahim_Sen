# EE413 Coding Theory: A Hybrid Error-Correction System

This repository presents the design and implementation of a multi-stage simulation platform developed for the EE413 Coding Theory course. The project evaluates the bit error rate (BER) performance of a serially concatenated error-correction system over a noisy medium, mapping a systematic linear block code as the outer stage and a continuous convolutional code as the inner stage.

## System Architecture

The simulation platform models a complete digital communication link utilizing the following topological data flow:

1. **Source Generation:** Converts personal identification strings directly into uniform binary streams.
2. **Outer Encoder:** Systematic Hamming (7,4) block encoder with localized single-bit error correction capability.
3. **Inner Encoder:** Rate R=1/2, constraint length K=3 convolutional encoder using generators g1(D) = D^2 + 1 and g2(D) = D^2 + D + 1 with dynamic zero-termination padding.
4. **Channel Noise:** Binary Symmetric Channel (BSC) mapping variable cross-over error probabilities.
5. **Inner Decoder:** Hard-decision Viterbi maximum-likelihood algorithm driven by Add-Compare-Select (ACS) loops and dynamic traceback operations.
6. **Outer Decoder:** Syndrome lookup table engine isolating and rectifying residual systematic block distortions.

## File Structure

* `main.py` - Core driver script containing the parametric test execution loops, ASCII bit conversion, and matplotlib visualization layers.
* `hamming.py` - Systematic generator matrix configurations, syndrome computation metrics, and single-bit coset lookup corrections.
* `convolutional.py` - Parametric state-transition encoders with dynamic zero-termination and the complete Viterbi trellis decoding engine.
* `channel.py` - Probabilistic Binary Symmetric Channel (BSC) noise injector and bit error verification metrics.

## Installation & Execution

### Prerequisites
The project requires Python 3.x along with `numpy` for matrix calculations and `matplotlib` for generating performance plots. You can install the dependencies via pip:

```bash
pip install numpy matplotlib