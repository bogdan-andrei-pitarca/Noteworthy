---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:1350
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: creamy floral with sweet orchard fruit and warm woods
  sentences:
  - 'violette-eau-de-parfum by molinard. Notes: . It smells like ripe peaches and
    white flowers at first, then soft rose petals, finishing with a hint of powdery
    musk.'
  - 'choco-exclusif by vivamor-parfums. Notes: . It smells like sweet orange peel
    and bergamot at first, then dark chocolate and vanilla, with a hint of vanilla
    sweetness underneath.'
  - 'burberry-women by burberry. Notes: . It smells like sweet peaches and apricots
    at first, then white flowers and powdery sandalwood, finishing with something
    earthy and slightly woody.'
- source_sentence: smells like a leather-bound book in a cedar library
  sentences:
  - 'signorina-eau-de-toilette by salvatore-ferragamo. Notes: . It smells like ripe
    citrus and white flowers at first, then settles into creamy milk mousse with a
    hint of powdery sweetness.'
  - 'forever-mine-into-the-legend-for-men by chevignon. Notes: . It smells like orange
    peel and citrus peel at first, then warm leather and soft wood, finishing with
    a hint of earthy wood.'
  - 'dior-homme-intense-2011 by dior. Notes: . It smells like dried lavender and iris
    at first, then soft pear and sweet vanilla, with a warm, slightly earthy base.'
- source_sentence: cozy vanilla with exotic spice market edge
  sentences:
  - 'colonia-intensa-oud-eau-de-cologne-concentree by acqua-di-parma. Notes: . It
    smells like a leather jacket left in an old wooden shed, with something earthy
    and slightly musky underneath.'
  - 'f-by-ferragamo-black by salvatore-ferragamo. Notes: . It smells like a spice
    market at dawn — sweet lavender and citrus peel mixed with powdery black pepper,
    finishing with something earthy and slightly floral.'
  - 'kenzo-jungle-l-elephant by kenzo. Notes: . It smells like cloves and citrus peel
    at first, then sweet vanilla and powdery licorice, finishing with a warm, slightly
    earthy base.'
- source_sentence: sunny beach vacation with fresh flowers and warm sand
  sentences:
  - 'crystal-noir by versace. Notes: . It smells like a spice market at dawn — sweet
    pepper and cardamom mixed with white flowers, then soft wood and something earthy-musky.'
  - 'loverdose by diesel. Notes: . It smells like sweet orange peel and citrus peel
    at first, then white flowers with a hint of vanilla and woodsy notes.'
  - 'nirmala by molinard. Notes: . It smells like citrus peel and mango at first,
    then white flowers and jasmine, finishing with something earthy and slightly woody.'
- source_sentence: gardenia bouquet with warm vanilla and aged wood
  sentences:
  - 'djhenne-22 by pierre-guillaume-paris. Notes: . It smells like powdery lavender
    and mint at first, then creamy white flowers with a hint of honeyed wood.'
  - 'hypnose by lancome. Notes: . It smells like a flower shop next to an old church
    — white flowers blooming in the background, with something faintly floral and
    slightly woody underneath.'
  - 'tabacco-toscano by santa-maria-novella. Notes: . It smells like a leather jacket
    left in an old wooden shed, where tobacco leaves sit next to birch trees, with
    something earthy and slightly woody lurking in the background.'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- pearson_cosine
- spearman_cosine
model-index:
- name: SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2
  results:
  - task:
      type: semantic-similarity
      name: Semantic Similarity
    dataset:
      name: fragrance eval
      type: fragrance-eval
    metrics:
    - type: pearson_cosine
      value: 0.5860045897062588
      name: Pearson Cosine
    - type: spearman_cosine
      value: 0.5966763686498697
      name: Spearman Cosine
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'gardenia bouquet with warm vanilla and aged wood',
    'hypnose by lancome. Notes: . It smells like a flower shop next to an old church — white flowers blooming in the background, with something faintly floral and slightly woody underneath.',
    'djhenne-22 by pierre-guillaume-paris. Notes: . It smells like powdery lavender and mint at first, then creamy white flowers with a hint of honeyed wood.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.3118, 0.3009],
#         [0.3118, 1.0000, 0.3902],
#         [0.3009, 0.3902, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

## Evaluation

### Metrics

#### Semantic Similarity

* Dataset: `fragrance-eval`
* Evaluated with [<code>EmbeddingSimilarityEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.EmbeddingSimilarityEvaluator)

| Metric              | Value      |
|:--------------------|:-----------|
| pearson_cosine      | 0.586      |
| **spearman_cosine** | **0.5967** |

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 1,350 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                         |
  |:--------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                            | string                                                                             |
  | details | <ul><li>min: 8 tokens</li><li>mean: 11.36 tokens</li><li>max: 18 tokens</li></ul> | <ul><li>min: 31 tokens</li><li>mean: 44.78 tokens</li><li>max: 70 tokens</li></ul> |
* Samples:
  | sentence_0                                                       | sentence_1                                                                                                                                                                                                                    |
  |:-----------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>soft powdery jasmine bedtime scent</code>                  | <code>memoire-d-une-odeur by gucci. Notes: . It smells like chamomile and mint at first, then soft jasmine and vanilla, with a hint of powdery wood underneath.</code>                                                        |
  | <code>smells like a leather-bound book in a cedar library</code> | <code>forever-mine-into-the-legend-for-men by chevignon. Notes: . It smells like orange peel and citrus peel at first, then warm leather and soft wood, finishing with a hint of earthy wood.</code>                          |
  | <code>green florals meeting smoky temple air</code>              | <code>de-profundis-limited-edition by serge-lutens. Notes: . It smells like a flower shop next to an incense stand — green flowers and violets mixed with white flowers, then settles into something earthy and woody.</code> |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 64
- `per_device_eval_batch_size`: 64
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `do_predict`: False
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 64
- `per_device_eval_batch_size`: 64
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 3
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_ratio`: None
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `enable_jit_checkpoint`: False
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `use_cpu`: False
- `seed`: 42
- `data_seed`: None
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: -1
- `ddp_backend`: None
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `auto_find_batch_size`: False
- `full_determinism`: False
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `use_cache`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch | Step | fragrance-eval_spearman_cosine |
|:-----:|:----:|:------------------------------:|
| 1.0   | 22   | 0.4785                         |
| 2.0   | 44   | 0.5706                         |
| 3.0   | 66   | 0.5967                         |


### Training Time
- **Training**: 11.1 seconds

### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.4.1
- Transformers: 5.0.0
- PyTorch: 2.10.0+cu128
- Accelerate: 1.13.0
- Datasets: 4.0.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->