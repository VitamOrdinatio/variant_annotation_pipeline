# README.md for `docs/case_studies/hg002/benchmarking/`

To calculate aggregate metrics across SNP and INDEL performance for VAP on HG002, we employed the following procedure.

From the [hg002 SNP indel metrics TSV](hg002_snp_indel_metrics.tsv):

| Variant Type |  TRUTH.TP | TRUTH.FN | QUERY.FP |
| ------------ | --------: | -------: | -------: |
| SNP          | 3,294,402 |   70,713 |   48,167 |
| INDEL        |   445,168 |   80,298 |   26,168 |

Note that:

- `QUERY.TP` was absent, so the v1 fallback used `TRUTH.TP` as `TP`.

---

## Step 1: Aggregate TP

```text
TP = SNP_TP + INDEL_TP
TP = 3,294,402 + 445,168
TP = 3,739,570
```

---

## Step 2: Aggregate FP

```text
FP = SNP_FP + INDEL_FP
FP = 48,167 + 26,168
FP = 74,335
```

---

## Step 3: Aggregate FN

```text
FN = SNP_FN + INDEL_FN
FN = 70,713 + 80,298
FN = 151,011
```

---

## Step 4: Quick Validation Aginst Final Benchmark Summary

```text
TP = 3,739,570
FP =   74,335
FN =  151,011
```

The [Final Benchmark Summary](hg002_benchmark_summary.json) thus validates these aggregate calculations.

---

## Step 5: Precision

Precision formula:


```text
                TP
Precision =  ———————
             TP + FP
```
	​
Substitute values:

```text
                  3,739,570
Precision =  —————————————————— = 0.9805094778
             3,739,570 + 74,335
```

Rounded:

```text
Precision = 0.9805
Precision = 98.05%
```

---

## Step 6: Recall

Recall formula:

```text
            TP
Recall =  ———————
          TP + FN
```

Substitute:

```text
               3,739,570
Recall =  ——————————————————— = 0.9611854887
          3,739,570 + 151,011
```

Rounded:

```text
Recall = 0.9612
Recall = 96.12%
```

---

## Step 7: F1

```text
       2PR
F1 =  ——————
      P + R
```

Using:

```text
P = 0.9805094778
R = 0.9611854887
```

Numerator:

```text
2 × P × R = 2 × 0.9805094778 × 0.9611854887
2PR = 1.8858477009
```

Denominator:

```text
P + R = 0.9805094778 + 0.9611854887
P + R = 1.9416949665
```

Final:

```text
       2PR      1.8858477009
F1 =  —————— =  ———————————— = 0.9707513259
      P + R     1.9416949665
```

Rounded:

```text
F1 = 0.9707513259
F1 = 97.08%
```

---

# Final aggregate values

```text
TP = 3,739,570
FP =   74,335
FN =  151,011

Precision = 0.9805 (98.05%)
Recall    = 0.9612 (96.12%)
F1        = 0.9708 (97.08%)
```

> `hap.py` benchmarking reveals that VAP performance on HG002 exhibits robust precision, recall and F1 metrics.