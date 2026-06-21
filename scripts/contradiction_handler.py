def analyze_source_mix(results):

    #Check which source types made it into the final context
    source_types = {
        result.get("source_type", "")
        for result in results
    }

    has_documentation = "documentation" in source_types
    has_blog = "blog" in source_types
    has_forum = "forum" in source_types

    has_lower_authority_sources = has_blog or has_forum

    #If official docs and community sources are both present,
    #there is a possibility of conflicting guidance
    conflict_possible = has_documentation and has_lower_authority_sources

    return {
        "conflict_possible": conflict_possible,
        "source_types": list(source_types),
        "resolution_strategy": (
            "Official documentation is prioritized over blog and forum content."
            if conflict_possible
            else None
        )
    }


def build_contradiction_note(conflict_info):

    #Only add note when multiple authority levels were used
    if not conflict_info["conflict_possible"]:
        return ""

    return (
        "\n\nSource Priority:\n"
        "Sources were ranked by authority before answer generation. "
        "When potentially conflicting information was retrieved, "
        "higher-authority sources were prioritized."
    )