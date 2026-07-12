"""
Canonical VAP variant-identity construction.

This module centralizes the existing VAP v1 coordinate/allele identifier
serialization used by Stage 07 and future sibling evidence projections.

Important
---------
Version 1 deliberately performs no normalization, validation, case
conversion, contig rewriting, allele decomposition, or symbolic-allele
interpretation. It preserves the exact legacy Stage 07 behavior:

    chromosome:position:reference_allele:alternate_allele
"""

from __future__ import annotations


def build_variant_id(
    chromosome: str,
    position: str,
    reference_allele: str,
    alternate_allele: str,
) -> str:
    """
    Build the canonical VAP v1 variant identifier.

    Parameters
    ----------
    chromosome
        Chromosome or contig token exactly as supplied by the caller.
    position
        Position token exactly as supplied by the caller.
    reference_allele
        Reference allele exactly as supplied by the caller.
    alternate_allele
        Alternate allele field exactly as supplied by the caller.

    Returns
    -------
    str
        Identifier in the legacy VAP v1 form:
        ``chromosome:position:reference_allele:alternate_allele``.

    Notes
    -----
    This function is serialization-only. It does not assert that the input
    is normalized, biallelic, biologically valid, or tied to a particular
    reference build.
    """
    return (
        f"{chromosome}:{position}:"
        f"{reference_allele}:{alternate_allele}"
    )
