---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:1000
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: It smells like sweet peach and bright citrus at first, then creamy
    white flowers take over, settling into soft wood and warm vanilla-like resin.
  sentences:
  - cherry, melon, raspberry, red rose, peony, orange blossom, hazelnut, musk, amber
  - white peach, sicilian mandarin, ylang-ylang, jasmine, benzoin, cedar
  - violet, sea notes, banana leaf, petitgrain, violet, magnolia, lily-of-the-valley,
    tuberose, pepper, incense, sandalwood, madagascar vanilla, myrrh
- source_sentence: It smells like crushed purple fruit mixed with dusty pink flowers
    and old wooden furniture, leaving a sticky-sweet resinous trail on your clothes.
  sentences:
  - plum, geranium, bergamot, patchouli, rose, benzoin, amber, sandalwood, musk
  - rice, anise, bourbon pepper, coffee, orange blossom, coriander, peony, vanilla,
    milk, caramel, sandalwood, white musk
  - green notes, rice flower, iris, bergamot, lotus, rhubarb, lily, ginger, orchid,
    musk, sandalwood, amber
- source_sentence: It smells like crushed green leaves and cardamom spice, then sweet
    almond paste with white flowers, finishing with a soft powdery musk.
  sentences:
  - bitter orange, lemon, damask rose, grasse rose, orange blossom, vanilla, almond,
    tonka bean, tolu balsam, sandalwood, cashmeran, heliotrope
  - violet leaf, cardamom, red currant, almond, lily-of-the-valley, jasmine, heliotrope,
    musk, benzoin
  - peach, bergamot, aldehydes, cambodian oud, carnation, patchouli, angelica, russian
    leather, musk, amber, oakmoss, patchouli
- source_sentence: It smells like black licorice and citrus peel at first, then softens
    into creamy vanilla with dry wood and a faint almond sweetness underneath.
  sentences:
  - licorice, citruses, grapefruit, bergamot, lavender, star anise, vanilla, almond,
    sandalwood, amber, cedar
  - orange, floral notes, violet, caramel, vanilla, moss
  - lemon, peach, ginger, mandarin orange, lavender, bergamot, pepper, cedar, patchouli,
    vetiver, brazilian rosewood, rose, jasmine, gardenia, freesia, anise, vanilla,
    tonka bean, sandalwood, coconut, amber, benzoin, musk, leather, oakmoss
- source_sentence: It smells like standing on a weathered dock at dawn — citrus cutting
    through salt air, wet wood, and that clean mineral scent of ocean spray drying
    on your arms.
  sentences:
  - orange, bergamot, grapefruit, litchi, rose, italian jasmine, patchouli, tahitian
    vetiver, bourbon vanilla, white musk
  - cucumber, mandarin orange, cassia, water hyacinth, carrot, white woods, sandalwood
  - bergamot, lemon, seaweed, calone, hedione, musk, ambroxan, cedar
pipeline_tag: sentence-similarity
library_name: sentence-transformers
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
    'It smells like standing on a weathered dock at dawn — citrus cutting through salt air, wet wood, and that clean mineral scent of ocean spray drying on your arms.',
    'bergamot, lemon, seaweed, calone, hedione, musk, ambroxan, cedar',
    'cucumber, mandarin orange, cassia, water hyacinth, carrot, white woods, sandalwood',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.3344, 0.3423],
#         [0.3344, 1.0000, 0.6667],
#         [0.3423, 0.6667, 1.0000]])
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

* Size: 1,000 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                         | sentence_1                                                                         |
  |:--------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                             | string                                                                             |
  | details | <ul><li>min: 19 tokens</li><li>mean: 32.78 tokens</li><li>max: 53 tokens</li></ul> | <ul><li>min: 7 tokens</li><li>mean: 33.31 tokens</li><li>max: 103 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                         | sentence_1                                                                                                                                                                                                                                                                                                           |
  |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>It smells like a worn leather jacket left in a cedar closet, with hints of bitter citrus peel and the dusty, resinous scent of old wooden furniture.</code>                                  | <code>grapefruit, lavender, artemisia, tobacco, spices, leather, agarwood (oud), dark woodsy notes, ambergris</code>                                                                                                                                                                                                 |
  | <code>It smells like a leather jacket someone wore to a dimly lit bar where spiced berry cocktails were being poured, with something slightly medicinal and woody lingering in the corners.</code> | <code>blackberry, rum, saffron, leather, agarwood (oud), clary sage, patchouli, musk</code>                                                                                                                                                                                                                          |
  | <code>It smells like a bouquet of white flowers and jasmine over something green and slightly bitter, with dry incense smoke and soft leather in the background.</code>                            | <code>white lily, hiacynth, honeysuckle, galbanum, orange blossom, lavender, bergamot, black currant, lemon, lily, lily-of-the-valley, moroccan jasmine, carnation, honeysuckle, tuberose, ylang-ylang, iris, rose, orris root, oakmoss, incense, musk, leather, sandalwood, vetiver, cedar, patchouli, amber</code> |
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

- `per_device_train_batch_size`: 32
- `per_device_eval_batch_size`: 32
- `num_train_epochs`: 4
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 32
- `per_device_eval_batch_size`: 32
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 4
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

### Training Time
- **Training**: 15.0 seconds

### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.4.0
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