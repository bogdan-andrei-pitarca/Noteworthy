---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:1323
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: sweet powdered sugar over dark roasted beans
  sentences:
  - 'Accords: coffee, powdery, musky. Notes: angelica, pink pepper, passionfruit,
    violet leaf, bergamot, coffee, vanilla, jasmine.'
  - 'Accords: amber, sweet, warm spicy. Notes: blackberry, olibanum, orange, labdanum,
    coriander, tarragon, honey, guaiac wood. Profile: It smells like ripe blackberries
    and orange peel at first, then sweet vanilla and honey, finishing with a hint
    of powdery florals and warm wood..'
  - 'Accords: coffee, warm spicy, fruity. Notes: black currant, pink pepper, tuberose,
    magnolia, coffee, tonka bean, sandalwood. Profile: It smells like a coffee shop
    at dawn — sweet black currants mixed with powdered sugar, then softened by warm
    vanilla and earthy wood..'
- source_sentence: walking into a flower shop early morning
  sentences:
  - 'Accords: coconut, sweet, woody. Notes: coconut, pineapple, lime, apple, bergamot,
    orange, cedar, geranium.'
  - 'Accords: caramel, soft spicy, amber. Notes: pink pepper, citruses, davana, rum,
    blackberry, caramel, white flowers, osmanthus. Profile: It smells like a spice
    market at dawn — sweet peppercorns mixed with white flowers, then softened by
    something earthy and slightly powdery..'
  - 'Accords: coconut, powdery, sweet. Notes: solar notes, bergamot, peach, heliotrope,
    lily-of-the-valley, coconut, musk, cedar. Profile: It smells like a flower shop
    at dawn — sweet peaches and bergamot mixed with powdery flowers, then softened
    by something earthy and slightly woody..'
- source_sentence: creamy almond dessert with fresh pear slices
  sentences:
  - 'Accords: almond, sweet, nutty. Notes: pistachio, pear, mandarin orange, almond,
    orange blossom, magnolia, almond milk, tonka bean. Profile: It smells like ripe
    pear and orange peel at first, then soft almond milk and vanilla, with a creamy
    sweetness that''s slightly sweet..'
  - 'Accords: almond, woody, fruity. Notes: amaretto, bitter almond, gardenia, neroli,
    cedar, iris, musk, jasmine.'
  - 'Accords: cacao, vanilla, white floral. Notes: gardenia, cacao, vanilla. Profile:
    It smells like a spice market at dawn — sweet tropical fruits mixed with vanilla
    and powdered sugar..'
- source_sentence: sweet citrus opening that becomes creamy vanilla woods
  sentences:
  - 'Accords: almond, vanilla, powdery. Notes: almond, brazilian rosewood, rose, geranium,
    plum, virginia cedar, celery, heliotrope. Profile: It smells like sweet almonds
    and roses at first, then creamy white flowers, with a hint of earthy musk underneath..'
  - 'Accords: fruity, sweet, fresh. Notes: passionfruit, peach, pear, raspberry, cassis,
    white flowers, lily-of-the-valley, vanilla.'
  - 'Accords: fruity, warm spicy, woody. Notes: plum, apple, grapefruit, bergamot,
    cinnamon, pink pepper, cardamom, juniper. Profile: It smells like ripe plums and
    citrus peel at first, then sweet vanilla and powdery spice, finishing with a warm,
    slightly woody base..'
- source_sentence: fresh citrus mint with sweet powder and earthy woods
  sentences:
  - 'Accords: amber, woody, citrus. Notes: lavender, mandarin orange, bergamot, geranium,
    hedione, violet, jasmine, coriander. Profile: It smells like sweet lavender and
    citrus peel at first, then white flowers and vanilla, finishing with a soft woody
    base..'
  - 'Accords: aromatic, warm spicy, patchouli. Notes: coriander, cardamom, bergamot,
    rose, jasmine, ylang-ylang, patchouli, musk.'
  - 'Accords: aromatic, citrus, green. Notes: amalfi lemon, mint, water jasmine, virginia
    cedar, brown sugar, french labdanum. Profile: It smells like fresh lemon and mint
    at first, then white flowers with a hint of powdered sugar, finishing with something
    earthy and slightly sweet..'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- cosine_accuracy
model-index:
- name: SentenceTransformer based on sentence-transformers/all-mpnet-base-v2
  results:
  - task:
      type: triplet
      name: Triplet
    dataset:
      name: fragrance triplet v3
      type: fragrance-triplet-v3
    metrics:
    - type: cosine_accuracy
      value: 1.0
      name: Cosine Accuracy
---

# SentenceTransformer based on sentence-transformers/all-mpnet-base-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) <!-- at revision e8c3b32edf5434bc2275fc9bab85f82640a19130 -->
- **Maximum Sequence Length:** 384 tokens
- **Output Dimensionality:** 768 dimensions
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
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'MPNetModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
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
    'fresh citrus mint with sweet powder and earthy woods',
    'Accords: aromatic, citrus, green. Notes: amalfi lemon, mint, water jasmine, virginia cedar, brown sugar, french labdanum. Profile: It smells like fresh lemon and mint at first, then white flowers with a hint of powdered sugar, finishing with something earthy and slightly sweet..',
    'Accords: aromatic, warm spicy, patchouli. Notes: coriander, cardamom, bergamot, rose, jasmine, ylang-ylang, patchouli, musk.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[ 1.0000,  0.6890, -0.0704],
#         [ 0.6890,  1.0000,  0.0608],
#         [-0.0704,  0.0608,  1.0000]])
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

#### Triplet

* Dataset: `fragrance-triplet-v3`
* Evaluated with [<code>TripletEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.TripletEvaluator)

| Metric              | Value   |
|:--------------------|:--------|
| **cosine_accuracy** | **1.0** |

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

* Size: 1,323 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>sentence_2</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                         | sentence_2                                                                         |
  |:--------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                            | string                                                                             | string                                                                             |
  | details | <ul><li>min: 7 tokens</li><li>mean: 11.11 tokens</li><li>max: 17 tokens</li></ul> | <ul><li>min: 41 tokens</li><li>mean: 68.66 tokens</li><li>max: 97 tokens</li></ul> | <ul><li>min: 20 tokens</li><li>mean: 36.54 tokens</li><li>max: 54 tokens</li></ul> |
* Samples:
  | sentence_0                                                                 | sentence_1                                                                                                                                                                                                                                                                       | sentence_2                                                                                                                                                              |
  |:---------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>spice market with soft flowers and warm wood</code>                  | <code>Accords: fresh spicy, rose, warm spicy. Notes: black pepper, cardamom, caraway, rose, nutmeg, sandalwood. Profile: It smells like a spice market at dawn — sweet pepper and cardamom mixed with white flowers, finishing with something earthy and slightly woody..</code> | <code>Accords: fresh spicy, aromatic, woody. Notes: pink pepper, pepper, geranium, elemi, nutmeg, incense, vetiver, virginia cedar.</code>                              |
  | <code>romantic rose garden with vanilla sweetness and golden warmth</code> | <code>Accords: amber, patchouli, rose. Notes: mandarin orange, turkish rose, bulgarian rose, amber, patchouli, vanilla. Profile: It smells like citrus peel and orange peel at first, then rose petals and amber, finishing with a warm vanilla-vanilla base..</code>            | <code>Accords: amber, vanilla, white floral. Notes: pink pepper, pink grapefruit, freesia, heliotrope, jasmine, lily-of-the-valley, siam benzoin, cashmere wood.</code> |
  | <code>sweet cinnamon and earthy warmth with soft floral edges</code>       | <code>Accords: cinnamon, warm spicy, amber. Notes: cinnamon, tangerine, plum, mimosa, amber, patchouli. Profile: It smells like a spice market at dawn — sweet cinnamon and orange peel mixed with powdery amber, finishing with something earthy and slightly floral..</code>   | <code>Accords: cinnamon, warm spicy, amber. Notes: bergamot, cinnamon, juniper berries, incense.</code>                                                                 |
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

### Training Logs
| Epoch | Step | fragrance-triplet-v3_cosine_accuracy |
|:-----:|:----:|:------------------------------------:|
| -1    | -1   | 0.8503                               |
| 1.0   | 42   | 1.0                                  |


### Training Time
- **Training**: 43.6 seconds

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