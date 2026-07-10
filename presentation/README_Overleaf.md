# FedHome Presentation - Overleaf Upload Instructions

## Files to Upload to Overleaf

Upload the following files from the `presentation/` directory:

### Required Files
1. `presentation.tex` - Main LaTeX file
2. `figures/auc_convergence_fullscale.png` - AUC convergence figure
3. `figures/client_auc_distribution.png` - Client distribution figure
4. `figures/client_auc_heatmap.png` - Heatmap figure
5. `figures/training_time_per_round.png` - Training time figure

## Overleaf Setup

### Compiler Settings
- **Compiler:** pdfLaTeX
- **TeX Live version:** 2023 or later

### How to Compile
1. Create a new project on Overleaf
2. Upload all files listed above
3. Keep the folder structure (create a `figures/` folder)
4. Click "Recompile" - the presentation should compile without errors

## Presentation Structure

| Section | Slides | Content |
|---------|--------|---------|
| Framework/Methodology | 6 slides | Problem statement, FedHome architecture, 4-phase pipeline |
| Implementation | 5 slides | Technology stack, Spark configuration, code snippets |
| Experimental Results | 5 slides | 4 figures showing AUC convergence, distribution, heatmap, training time |
| Conclusion | 2 slides | Summary, future work, Q&A |
| Appendix | 1 slide | Repository structure |
| **Total** | **19 slides** | |

## Requirements Checklist

| Requirement | Minimum | Provided | Status |
|-------------|---------|----------|--------|
| Framework/Methodology slides | 3 | 6 | ✅ Exceeded |
| Implementation slides | 3 | 5 | ✅ Exceeded |
| Experimental Results slides | 2 | 5 | ✅ Exceeded |
| Figures showing output | 2 | 4 | ✅ Exceeded |

## Key Results to Highlight

- **Average AUC:** 0.9829 (exceeded 0.97 target)
- **Loss Reduction:** 41.0%
- **Training Time:** 2.87 minutes for 20 rounds
- **All 50 clients** completed successfully

## Troubleshooting

### If figures don't show
- Ensure the `figures/` folder exists in Overleaf
- Check that all `.png` files are uploaded
- Verify file names match exactly (case-sensitive)

### If compilation fails
- Use pdfLaTeX compiler
- Check that all packages are available (standard Beamer packages)
- Clear cached files and recompile

## Contact
Md. Raihan Sobhan - Big Data Analytics Course Project
