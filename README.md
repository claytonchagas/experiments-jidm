experiments-jidm
================

Scripts of the multi-script evaluation (Section 7) of the paper *On the Importance of Modularization to the Meaningfulness of Provenance from Scripts* (Journal of Information and Data Management). The companion website of the paper is https://gems-uff.github.io/pypofacets, where the re-execution package (provenance graphs, metrics, and analysis scripts) and the prompts are published.

Six algorithms were used in the paper: `belief_propagation`, `cvar`, `fft`, `gauss_legendre_quadrature`, `heat_distribution_lu`, and `look_and_say`. Each folder contains:

* `<name>.py`: expert version, written by the original authors of the script (the memoization decorators and imports of the study for which the corpus was assembled were removed);
* `<name>_claude.py`: monolithic baseline, generated from the expert version by Claude Opus 4.6 (GitHub Copilot Chat, February 2026) by inlining every user-defined function;
* `<name>_claude_modular.py`: LLM-modularized version, generated from the monolithic baseline by the same model;
* `dataflows/`: the dataflow graphs of the original executions of the three versions, as `.dot` and `.svg`; the graphs reported in the paper (noWorkflow 2.1.1, `now export dataflow <trial> -d 1`, inputs below) are in the re-execution package of the companion website (`multiscript/dataflows/`), and for CVaR and FFT they differ from these because the inputs were changed.

Inputs used in the paper (one argument per script): belief_propagation 20, cvar 50, fft 500, gauss_legendre_quadrature 50, heat_distribution_lu 1, look_and_say 5. Heat Distribution relies on the auxiliary modules `model.py`, `solver.py`, `fatoracao_lu.py`, and `heat_map.py`, kept identical across the three versions.

The files `<name>_chatgpt.py` and `<name>_gemini.py` are monolithic versions produced by other LLMs during the preparation of the study; they were not used in the paper. The folders `diversity_sims`, `dnacc`, `epr`, and `tiny` hold four other scripts of the same corpus, left for future work. The folder `_pypofacets` holds the copies of the PyPOFacets scripts used to compute the soft-matching similarities (`compare_functions.py`, `similarity.txt`).
