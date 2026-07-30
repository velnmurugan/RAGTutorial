# Projects

A selection of research and coursework projects. Code for all of these
is on [GitHub](https://github.com/velnmurugan).

## [Complex-Valued U-Net for Fourier Ptychographic Microscopy](https://github.com/velnmurugan/FPM)

A physics-informed complex-valued U-Net that reconstructs high-resolution
amplitude and phase images from low-resolution FPM microscope
measurements — replacing the usual iterative phase-retrieval optimization
with a model that learns the reconstruction directly while staying
consistent with the underlying physics.

## [Polygon Corner Prediction](https://github.com/velnmurugan/polygon-transformer)

A lightweight (under 5M parameters) PyTorch model that predicts ordered
polygon corner coordinates from 128×128 grayscale images. Includes a full
training pipeline, a custom variable-length dataset loader, and
polygon-IoU evaluation.

## [Bi-Molecular Coupling Energy Prediction](https://github.com/velnmurugan/Bimolecule_quantum_kernel)

Predicts coupling energies for molecule-pair geometries using classical
Kernel Ridge Regression on Coulomb-matrix features, benchmarked against a
quantum kernel baseline built with PennyLane (quantum feature map + state
overlap kernel). Includes grouped evaluation to avoid data leakage.

## [Denoising Microscopic Images with Noise2Void](https://github.com/velnmurugan/Image-denoising)

Self-supervised denoising of microscopy images using a blind-spot U-Net
(Noise2Void) — learns to denoise from a single noisy image, no clean
ground truth required.

## [Bayesian Inference for Climate Reconstruction](https://github.com/velnmurugan/bayesian-climate-reconstruction-challenge)

Solves an ill-posed inverse problem analogous to paleoclimate
reconstruction: recovering an unknown boundary condition from noisy
interior measurements of a steady-state heat equation. Uses Gaussian RBF
parameterization, Laplace approximation, and evidence-based
hyperparameter tuning for principled uncertainty quantification.

## [AugMix](https://github.com/velnmurugan/augmix)

Fork of Google Research's AugMix — a data augmentation method for
improving model robustness and uncertainty calibration.
