"""Fine-tune a HuggingFace BERT model for 3-class polarity.

This is the optional modern training path.  The faithful ktrain/Colab path is
documented in docs/TRAIN_POLARITY_MODEL.md.

Example (GPU recommended):
    python scripts/train_polarity.py --base-model bert-base-uncased --epochs 3
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATASET = PROJECT_ROOT / "Data" / "GeneratedData" / "LabeledNews.csv"
LABELS = ["Negative", "Neutral", "Positive"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", default="bert-base-uncased")
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--output", default=str(PROJECT_ROOT / "PythonObjects" / "PolarityClassifier"))
    args = parser.parse_args()

    import torch
    from datasets import Dataset
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        Trainer,
        TrainingArguments,
    )

    data = pd.read_csv(DATASET).dropna(subset=["News", "Sentiment"])
    label_to_id = {label: index for index, label in enumerate(LABELS)}
    data = data[data["Sentiment"].isin(LABELS)]
    train, test = train_test_split(
        data, test_size=0.2, random_state=0, stratify=data["Sentiment"]
    )
    train_dataset = Dataset.from_dict(
        {"text": train["News"].astype(str).tolist(), "label": [label_to_id[x] for x in train["Sentiment"]]}
    )
    test_dataset = Dataset.from_dict(
        {"text": test["News"].astype(str).tolist(), "label": [label_to_id[x] for x in test["Sentiment"]]}
    )
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=args.max_length)

    train_dataset = train_dataset.map(tokenize, batched=True)
    test_dataset = test_dataset.map(tokenize, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.base_model, num_labels=len(LABELS), id2label={i: l for i, l in enumerate(LABELS)}
    )

    def metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, predictions, average="weighted", zero_division=0
        )
        return {
            "accuracy": accuracy_score(labels, predictions),
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    training_args = TrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_steps=50,
        report_to=[],
        fp16=torch.cuda.is_available(),
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=metrics,
    )
    trainer.train()
    result = trainer.evaluate()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    (Path(args.output) / "training_metrics.json").write_text(
        json.dumps(result, indent=2, default=float), encoding="utf-8"
    )
    print(f"Saved model to {args.output}")
    print(json.dumps(result, indent=2, default=float))


if __name__ == "__main__":
    main()
