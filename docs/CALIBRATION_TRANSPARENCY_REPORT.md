# INFORME DE TRANSPARENCIA: SISTEMA DE CALIBRACIÓN Y PARAMETRIZACIÓN
**Estado**: FINAL | **Fuente de Verdad**: ÚNICA

## 1. Procedimiento Matemático de Calibración
El sistema utiliza una agregación de Choquet (o promedio ponderado en versión actual) sobre capas específicas determinadas por la naturaleza del método.

### Fórmula General
$$ Score_{final} = \frac{1}{N} \sum_{i=1}^{N} Score(Layer_i) $$

Donde $N$ es el número de capas requeridas para el tipo de método.

### Definición de Capas
- **@b**: Base Intrinsic Quality
- **@chain**: Chain Integrity
- **@u**: Unit Test Coverage
- **@m**: Metadata Completeness
- **@q**: Questionnaire Alignment
- **@d**: Dimensional Consistency
- **@p**: Policy Adherence
- **@C**: Congruence Check

## 2. Detalle de Métodos, Capas y Valores
| ID del Método | Tipo | Capas Requeridas (N) | Score Intrínseco (@b) | Parámetros Científicos |
| :--- | :--- | :---: | :---: | :--- |
| `executors.D1Q1_Executor.execute` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `module.Class.example_method` | processor | **4** (@b, @chain, @u, @m) | 0.652 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.BatchProcessor.export_batch_results` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.BatchProcessor.process_directory` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.CanonicalQuestionSegmenter.segment_plan` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.ConfigurationManager.load_config` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.ConfigurationManager.save_config` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.DocumentProcessor.load_canonical_question_contracts` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.DocumentProcessor.load_docx` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.DocumentProcessor.load_pdf` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.DocumentProcessor.segment_by_canonical_questionnaire` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.DocumentProcessor.segment_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.MunicipalAnalyzer.analyze_document` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.PerformanceAnalyzer.analyze_performance` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.ResultsExporter.export_summary_report` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.ResultsExporter.export_to_excel` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.ResultsExporter.export_to_json` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.Analyzer_one.SemanticAnalyzer.extract_semantic_cube` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.analysis.Analyzer_one.TextMiningEngine.diagnose_critical_links` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianPortfolioComposer.calculate_coverage` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianPortfolioComposer.compose_macro_portfolio` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianPortfolioComposer.export_to_csv` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianRollUp.aggregate_micro_to_meso` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianRollUp.export_to_csv` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianUpdater.export_to_csv` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianUpdater.sequential_update` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.BayesianUpdater.update` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ContradictionScanner.calculate_contradiction_penalty` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ContradictionScanner.scan_meso_macro` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ContradictionScanner.scan_micro_meso` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.DispersionEngine.calculate_cv` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.DispersionEngine.calculate_dispersion_penalty` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.DispersionEngine.calculate_gini` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.DispersionEngine.calculate_max_gap` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.MultiLevelBayesianOrchestrator.run_complete_analysis` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.PeerCalibrator.compare_to_peers` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ProbativeTest.calculate_likelihood_ratio` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.calculate_total_penalty` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.validate_data` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.validate_entity` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.validate_period` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.validate_range` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.bayesian_multilevel_system.ReconciliationValidator.validate_unit` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.contradiction_deteccion.BayesianConfidenceCalculator.calculate_posterior` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.contradiction_deteccion.PolicyContradictionDetector.detect` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.contradiction_deteccion.TemporalLogicVerifier.verify_temporal_consistency` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.AdaptivePriorCalculator.calculate_likelihood_adaptativo` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.AdaptivePriorCalculator.generate_traceability_record` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.AdaptivePriorCalculator.sensitivity_analysis` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.AdaptivePriorCalculator.validate_quality_criteria` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.BayesFactorTable.get_bayes_factor` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesFactorTable.get_version` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesianCounterfactualAuditor.aggregate_risk_and_prioritize` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesianCounterfactualAuditor.construct_scm` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesianCounterfactualAuditor.counterfactual_query` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesianCounterfactualAuditor.refutation_and_sanity_checks` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BayesianMechanismInference.infer_mechanisms` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.BeachEvidentialTest.apply_test_logic` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.BeachEvidentialTest.classify_test` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.CDAFException.to_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.CDAFFramework.process_document` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.CausalExtractor.extract_causal_hierarchy` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.CausalInferenceSetup.assign_probative_value` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.CausalInferenceSetup.classify_goal_dynamics` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.CausalInferenceSetup.identify_failure_points` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.check_uncertainty_reduction_criterion` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.get` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.get_bayesian_threshold` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.get_mechanism_prior` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.get_performance_setting` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ConfigLoader.update_priors_from_feedback` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.aggregate_risk` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.all_checks_passed` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.apply_test_logic` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.classify_test_type` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.construct_scm` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.counterfactual_query` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.create_auditor` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.create_hierarchical_model` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_ablation_curve` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_causal_effect` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_coherence_score` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_delta_waic` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_ess` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_independence_tests` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_model_preference` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_negative_controls` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_placebo_effect` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_ppc_recommendation` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_ppd_p_value` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_priority` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_r_hat` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_refutation_recommendation` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_risk_score` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_sanity_violations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_sequence_mode` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_success_probability` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.get_type_posterior` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.infer_mechanism_posterior` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_doubly_decisive` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_effect_stable` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_hoop_test` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_inference_uncertain` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_necessary` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_smoking_gun` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_straw_in_wind` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.is_sufficient` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.posterior_predictive_check` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.refutation_checks` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.DerekBeachProducer.verify_conditional_independence` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.FinancialAuditor.trace_financial_allocation` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.HierarchicalGenerativeModel.infer_mechanism_posterior` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.HierarchicalGenerativeModel.posterior_predictive_check` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.HierarchicalGenerativeModel.verify_conditional_independence` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.MechanismPartExtractor.extract_entity_activity` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.MechanismTypeConfig.check_sum_to_one` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.OperationalizationAuditor.audit_evidence_traceability` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.OperationalizationAuditor.audit_sequence_logic` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.OperationalizationAuditor.bayesian_counterfactual_audit` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.derek_beach.PDFProcessor.extract_sections` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.PDFProcessor.extract_tables` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.PDFProcessor.extract_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.PDFProcessor.load_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ReportingEngine.generate_accountability_matrix` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.derek_beach.ReportingEngine.generate_causal_diagram` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.ReportingEngine.generate_causal_model_json` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.derek_beach.ReportingEngine.generate_confidence_report` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.analyze_financial_feasibility` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.analyze_municipal_plan_sync` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.calculate_quality_score` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.construct_causal_dag` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.estimate_causal_effects` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.export_causal_network` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.generate_counterfactuals` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.generate_executive_report` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.generate_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.identify_responsible_entities` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer.sensitivity_analysis` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.macro_prompts.BayesianPortfolioComposer.compose` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.macro_prompts.ContradictionScanner.scan` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.macro_prompts.CoverageGapStressor.evaluate` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.macro_prompts.MacroPromptsOrchestrator.execute_all` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.macro_prompts.PeerNormalizer.normalize` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.macro_prompts.RoadmapOptimizer.optimize` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.analysis.meso_cluster_analysis.MetricViolation.to_flag_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.AntiMilagroStressTester.stress_test` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.AntiMilagroStressTester.to_json` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.BayesianPosteriorExplainer.explain` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.micro_prompts.BayesianPosteriorExplainer.to_json` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.analysis.micro_prompts.CausalChain.length` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.micro_prompts.ProvenanceAuditor.audit` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.ProvenanceAuditor.to_json` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.ProvenanceDAG.get_orphan_nodes` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.micro_prompts.ProvenanceDAG.get_root_nodes` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.Recommendation.to_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.export_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.generate_all_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.generate_macro_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.generate_meso_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.generate_micro_recommendations` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.get_thresholds_from_monolith` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationEngine.reload_rules` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.recommendation_engine.RecommendationSet.to_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.report_assembly.AnalysisReport.to_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.report_assembly.ReportAssembler.assemble_report` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.report_assembly.ReportAssembler.export_report` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.apply_scoring_modality` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.determine_quality_level` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_a` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_b` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_c` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_d` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_e` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.MicroQuestionScorer.score_type_f` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.scoring.ModalityConfig.validate_evidence` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.scoring.ScoredResult.compute_evidence_hash` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.scoring.ScoredResult.to_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.scoring.ScoringValidator.get_config` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.scoring.scoring.ScoringValidator.validate` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.spc_causal_bridge.SPCCausalBridge.build_causal_graph_from_spc` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.spc_causal_bridge.SPCCausalBridge.enhance_graph_with_content` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.add_edge` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.add_node` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.calculate_acyclicity_pvalue` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.export_nodes` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.get_graph_stats` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.last_serialized_nodes` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.AdvancedGraphNode.to_serializable_dict` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.IndustrialGradeValidator.execute_suite` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.IndustrialGradeValidator.run_performance_benchmarks` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.IndustrialGradeValidator.validate_causal_categories` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.teoria_cambio.IndustrialGradeValidator.validate_connection_matrix` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.IndustrialGradeValidator.validate_engine_readiness` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.analysis.teoria_cambio.TeoriaCambio.construir_grafo_causal` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.teoria_cambio.TeoriaCambio.construir_grafo_from_spc` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.analysis.teoria_cambio.TeoriaCambio.validacion_completa` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.api_server.DataService.get_evidence_stream` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.api_server.DataService.get_pdet_regions` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.api_server.DataService.get_region_detail` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.add_user` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.authenticate` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.change_password` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.cleanup_expired_sessions` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.get_session` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.logout` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminAuthenticator.validate_session` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminSession.is_expired` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.auth_admin.AdminSession.update_activity` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.pipeline_connector.PipelineConnector.get_job_status` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.api.pipeline_connector.PipelineConnector.get_result` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.executors.D1Q1_executor.D1Q1_Executor.execute` | executor | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.optimization.rl_strategy.BanditAlgorithm.select_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.mean_cost_usd` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.mean_duration_ms` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.mean_reward` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.sample_thompson` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.success_rate` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.to_dict` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.ucb_score` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.BanditArm.update` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.EpsilonGreedyAlgorithm.select_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.ExecutorMetrics.reward` | executor | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.add_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.get_statistics` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.load` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.print_summary` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.save` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.select_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.RLStrategyOptimizer.update` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.ThompsonSamplingAlgorithm.select_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.optimization.rl_strategy.UCB1Algorithm.select_arm` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.processing.aggregation.AggregationSettings.from_monolith` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.AreaPolicyAggregator.aggregate_area` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.AreaPolicyAggregator.apply_rubric_thresholds` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.AreaPolicyAggregator.normalize_scores` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.AreaPolicyAggregator.run` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.AreaPolicyAggregator.validate_hermeticity` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.ClusterAggregator.aggregate_cluster` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.ClusterAggregator.analyze_coherence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.ClusterAggregator.apply_cluster_weights` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.ClusterAggregator.run` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.ClusterAggregator.validate_cluster_hermeticity` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.aggregate_dimension` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.apply_rubric_thresholds` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.calculate_weighted_average` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.run` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.validate_coverage` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.validate_dimension_id` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.validate_policy_area_id` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.DimensionAggregator.validate_weights` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.MacroAggregator.apply_rubric_thresholds` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.MacroAggregator.assess_strategic_alignment` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.MacroAggregator.calculate_cross_cutting_coherence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.MacroAggregator.evaluate_macro` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.aggregation.MacroAggregator.identify_systemic_gaps` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.cpp_ingestion.models.ChunkGraph.add_chunk` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.cpp_ingestion.models.ChunkGraph.add_edge` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.DocumentLoader.extract_metadata` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.DocumentLoader.load_pdf` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.DocumentLoader.validate_pdf` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.DocumentLoader.validate_pdf_reader` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.PreprocessingEngine.detect_language` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.PreprocessingEngine.normalize_encoding` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.PreprocessingEngine.preprocess_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.TextExtractor.extract_by_page` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.TextExtractor.extract_full_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.document_ingestion.TextExtractor.preserve_structure` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.AdvancedSemanticChunker.chunk_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.BayesianNumericalAnalyzer.compare_policies` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.embedding_policy.BayesianNumericalAnalyzer.evaluate_policy_metric` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.embedding_policy.BayesianNumericalAnalyzer.serialize_posterior_samples` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.compare_policy_interventions` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.create_pdq_identifier` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.evaluate_numerical_consistency` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.generate_pdq_report` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_analytical_dimension_description` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_chunk_count` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_chunk_embedding` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_chunk_metadata` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_chunk_pdq_context` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_chunk_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_comparison_bayes_factor` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_comparison_difference_mean` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_comparison_probability` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_config` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_credible_interval` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_diagnostics` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_evidence_strength` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_numerical_coherence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_pdq_confidence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_pdq_evidence_count` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_pdq_evidence_passages` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_pdq_numerical_evaluation` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_point_estimate` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_policy_domain_description` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_search_result_chunk` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.get_search_result_score` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.list_analytical_dimensions` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.list_policy_domains` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.process_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingPolicyProducer.semantic_search` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.EmbeddingProtocol.encode` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.compare_policy_interventions` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.evaluate_policy_numerical_consistency` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.generate_pdq_report` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.get_diagnostics` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.process_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyAnalysisEmbedder.semantic_search` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.embedding_policy.PolicyCrossEncoderReranker.rerank` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.AdvancedTextSanitizer.sanitize` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.BayesianConfidenceCalculator.calculate_posterior` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.policy_processor.BayesianEvidenceScorer.compute_evidence_score` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.policy_processor.EvidenceBundle.to_dict` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.IndustrialPolicyProcessor.export_results` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.IndustrialPolicyProcessor.process` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.PolicyAnalysisPipeline.analyze_file` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.processing.policy_processor.PolicyAnalysisPipeline.analyze_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.processing.policy_processor.PolicyTextProcessor.compile_pattern` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.PolicyTextProcessor.extract_contextual_window` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.PolicyTextProcessor.normalize_unicode` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.PolicyTextProcessor.segment_into_sentences` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.ProcessorConfig.from_legacy` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.ProcessorConfig.validate` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.ResilientFileHandler.read_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.ResilientFileHandler.write_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor.TemporalLogicVerifier.verify_temporal_consistency` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.policy_processor._FallbackContradictionDetector.detect` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.BayesianEvidenceIntegrator.causal_strength` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.semantic_chunking_policy.BayesianEvidenceIntegrator.integrate_evidence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.processing.semantic_chunking_policy.PolicyDocumentAnalyzer.analyze` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.analyze_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.calculate_causal_strength` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.chunk_document` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.embed_batch` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.embed_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_chunk_count` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_chunk_embedding` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_chunk_metadata` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_chunk_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_confidence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_config` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_dimension_analysis` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_dimension_confidence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_dimension_description` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_dimension_excerpts` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_dimension_score` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_information_gain` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_posterior_mean` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.get_posterior_std` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.integrate_evidence` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.list_dimensions` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.semantic_search` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticChunkingProducer.set_config` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticProcessor.chunk_text` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.semantic_chunking_policy.SemanticProcessor.embed_single` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.processing.spc_ingestion.converter.SmartChunkConverter.convert_to_canon_package` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.spc_ingestion.quality_gates.SPCQualityGates.validate_chunks` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.spc_ingestion.quality_gates.SPCQualityGates.validate_input` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.spc_ingestion.quality_gates.SPCQualityGates.validate_output_compatibility` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.spc_ingestion.quality_gates.SPCQualityGates.validate_quality_metrics` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.processing.spc_ingestion.structural.StructuralNormalizer.normalize` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **CAUSAL**<br>Do-Depth=3 |
| `saaaaaa.utils.contract_io.ContractEnvelope.wrap` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts.AnalyzerProtocol.analyze` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts.DocumentLoaderProtocol.load_pdf` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts.DocumentLoaderProtocol.validate_pdf` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts.TextProcessorProtocol.normalize_unicode` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts.TextProcessorProtocol.segment_into_sentences` | processor | **4** (@b, @chain, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.contracts_runtime.SemanticAnalyzerInputModel.text_not_empty` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **SEMANTIC**<br>Dim=768 |
| `saaaaaa.utils.contracts_runtime.SemanticAnalyzerOutputModel.validate_probabilities` | analyzer | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **BAYESIAN**<br>Prior α=1.0, Cred=0.95 |
| `saaaaaa.utils.cpp_adapter.CPPAdapter.to_preprocessed_document` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.determinism.seeds.DeterministicContext.apply` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.determinism.seeds.DeterministicContext.from_factory` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.determinism.seeds.SeedFactory.configure_environment` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.determinism.seeds.SeedFactory.derive_run_seed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.determinism.seeds.SeedFactory.derive_seed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.deterministic_execution.DeterministicExecutor.deterministic` | executor | **8** (@b, @chain, @q, @d, @p, @C, @u, @m) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.deterministic_execution.DeterministicSeedManager.get_derived_seed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.deterministic_execution.DeterministicSeedManager.get_event_id` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.deterministic_execution.DeterministicSeedManager.scoped_seed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.AnalysisInputV2.create_from_text` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.AnalysisOutputV2.validate_confidence_numerical_stability` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.BaseContract.validate_timestamp` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.ProcessedTextV2.validate_input_digest` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.StructuredLogger.log_contract_validation` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.enhanced_contracts.StructuredLogger.log_execution` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.evidence_registry.EvidenceRecord.create` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.evidence_registry.EvidenceRegistry.append` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.evidence_registry.EvidenceRegistry.records` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.evidence_registry.EvidenceRegistry.save` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.evidence_registry.EvidenceRegistry.verify` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.json_contract_loader.ContractLoadReport.is_successful` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.json_contract_loader.ContractLoadReport.summary` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.json_contract_loader.JSONContractLoader.load` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.json_contract_loader.JSONContractLoader.load_directory` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.json_logger.JsonFormatter.format` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.metadata_loader.MetadataLoader.load_and_validate_metadata` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.method_config_loader.MethodConfigLoader.get_method_description` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.method_config_loader.MethodConfigLoader.get_method_parameter` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.method_config_loader.MethodConfigLoader.get_parameter_spec` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.method_config_loader.MethodConfigLoader.validate_parameter_value` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.method_config_loader.MethodConfigLoader.validate_spec_schema` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.clear_recording` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.disable` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.enable` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.get_statistics` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.load_recording` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.record_call` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.qmcm_hooks.QMCMRecorder.save_recording` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.PayloadValidator.validate` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.SchemaDriftDetector.get_alerts` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.SchemaDriftDetector.get_metrics` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.SchemaDriftDetector.record_payload` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.SchemaDriftDetector.save_baseline` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.schema_monitor.SchemaDriftDetector.should_sample` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.seed_factory.SeedFactory.configure_global_random_state` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.seed_factory.SeedFactory.create_deterministic_seed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.FunctionSignature.to_dict` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureAuditor.audit_module` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureAuditor.export_report` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.compute_signature_hash` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.get_signature` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.has_signature_changed` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.load` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.register_function` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.signature_validator.SignatureRegistry.save` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.aggregation_models.AggregationWeights.validate_non_negative` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.aggregation_models.AggregationWeights.validate_sum` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.aggregation_models.ClusterAggregationConfig.validate_policy_areas` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.aggregation_models.MacroAggregationConfig.validate_clusters` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.architecture_validator.ArchitectureValidationResult.to_dict` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.contract_logger.ContractErrorLogger.log_contract_mismatch` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.utils.validation.contract_logger.ContractErrorLogger.log_determinism_violation` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.utils.validation.contract_logger.ContractErrorLogger.log_invalid_modality` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.utils.validation.contract_logger.ContractErrorLogger.log_type_violation` | utility | **2** (@b, @chain) | 0.85 | **OPTIMIZATION**<br>LR=0.001 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.assert_atomic_context` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.assert_deterministic_dag` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.assert_homogeneous_treatment` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.assert_immutable_metadata` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.baseline_step_catalog` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.golden_rule.GoldenRuleValidator.reset_atomic_state` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.predicates.ValidationPredicates.verify_execution_context` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.predicates.ValidationPredicates.verify_expected_elements` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.predicates.ValidationPredicates.verify_producer_availability` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.predicates.ValidationPredicates.verify_scoring_preconditions` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.schema_validator.MonolithSchemaValidator.generate_validation_report` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation.schema_validator.MonolithSchemaValidator.validate_monolith` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.create_validation_report` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.validate_all_preconditions` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.validate_execution_context` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.validate_expected_elements` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.validate_producer_availability` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationEngine.validate_scoring_preconditions` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationReport.add_result` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationReport.has_errors` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |
| `saaaaaa.utils.validation_engine.ValidationReport.summary` | utility | **2** (@b, @chain) | 0.85 | **FREQUENTIST**<br>α=0.05, Power=0.8 |