# Projects

A selection of research and coursework projects. Code for all of these
is on [GitHub](https://github.com/velnmurugan).

::::{grid} 1 1 2 3

:::{card} Complex-Valued U-Net for FPM
:link: https://github.com/velnmurugan/FPM
:header: Computer Vision · Microscopy

A physics-informed complex-valued U-Net that reconstructs high-resolution
amplitude and phase images from low-resolution Fourier Ptychographic
Microscopy measurements — replacing iterative phase retrieval with a
model that learns the reconstruction directly.
+++
PyTorch · Physics-informed deep learning
:::

:::{card} Polygon Corner Prediction
:link: https://github.com/velnmurugan/polygon-transformer
:header: Computer Vision

A lightweight (under 5M parameters) model that predicts ordered polygon
corner coordinates from 128×128 grayscale images. Full training
pipeline, variable-length dataset loader, and polygon-IoU evaluation.
+++
PyTorch
:::

:::{card} Bi-Molecular Coupling Energy Prediction
:link: https://github.com/velnmurugan/Bimolecule_quantum_kernel
:header: Quantum ML · Chemistry

Predicts coupling energies for molecule-pair geometries using classical
Kernel Ridge Regression on Coulomb-matrix features, benchmarked against
a quantum kernel baseline built with PennyLane.
+++
scikit-learn · PennyLane
:::

:::{card} Denoising Microscopic Images
:link: https://github.com/velnmurugan/Image-denoising
:header: Computer Vision · Microscopy

Self-supervised denoising of microscopy images using a blind-spot U-Net
(Noise2Void) — learns to denoise from a single noisy image, no clean
ground truth required.
+++
TensorFlow · Noise2Void
:::

:::{card} Bayesian Climate Reconstruction
:link: https://github.com/velnmurugan/bayesian-climate-reconstruction-challenge
:header: Bayesian Inference

Solves an ill-posed inverse problem analogous to paleoclimate
reconstruction — recovering an unknown boundary condition from noisy
interior measurements, with evidence-based uncertainty quantification.
+++
NumPy · SciPy
:::

:::{card} AugMix
:link: https://github.com/velnmurugan/augmix
:header: Data Augmentation · Fork

Fork of Google Research's AugMix — a data augmentation method for
improving model robustness and uncertainty calibration.
+++
Python
:::

::::
