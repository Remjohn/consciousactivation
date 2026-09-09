### **intelligence/frameworks/viral\_trinity\_scoring.yaml**

Purpose: The scoring rubric used by The Premise Hunter to rank story potential.

Source: The Premise Hunter Agent

YAML

\# \==============================================================================  
\# VIRAL TRINITY SCORING RUBRIC (60-POINT SYSTEM)  
\# Used by: The Premise Hunter  
\# \==============================================================================

viral\_trinity:  
  total\_points: 40  
  dimensions:  
    surprise\_factor:  
      weight: 10  
      description: "The shock value of the revelation."  
      criteria:  
        9-10: "Shatters fundamental assumptions, shocking confession, complete worldview reversal."  
        7-8: "Unexpected twist, counter-intuitive insight, contrarian viewpoint."  
        5-6: "Somewhat surprising but predictable for informed audience."  
        3-4: "Mildly interesting, slight deviation from norm."  
        1-2: "Predictable, clichéd, expected outcome."  
      question: "Would this make someone stop mid-scroll and say 'Wait, WHAT?'"

    emotional\_intensity:  
      weight: 10  
      description: "The visceral feeling generated."  
      criteria:  
        9-10: "Visceral, brings tears/chills, immediately shareable, creates physical response."  
        7-8: "Strong emotional pull, memorable feeling, lingers after viewing."  
        5-6: "Pleasant emotion, not overwhelming, might forget in an hour."  
        3-4: "Mild emotional response, intellectually understood but not felt."  
        1-2: "Purely intellectual, no emotional engagement."  
      question: "Would this make someone feel something in their body, not just their head?"

    specificity:  
      weight: 10  
      description: "The richness of detail."  
      criteria:  
        9-10: "Vivid scene with sensory details, exact quotes, specific numbers, clear timeline."  
        7-8: "Good detail, enough concrete material to visualize and script."  
        5-6: "Some specifics present, but needs development or clarification."  
        3-4: "Vague statements, general concepts, missing concrete examples."  
        1-2: "Abstract theory, no tangible examples, purely conceptual."  
      question: "Can I see, hear, and feel this story? Could I draw a storyboard from this?"

    universal\_appeal:  
      weight: 10  
      description: "The breadth of relatability."  
      criteria:  
        9-10: "Every human being can relate to this core feeling/experience."  
        7-8: "Most people in the target demographic recognize this pattern."  
        5-6: "Relevant to a specific subset of the tribe."  
        3-4: "Niche experience, limited relatability."  
        1-2: "Highly specific circumstance, most people can't connect."  
      question: "How many people will think 'That's me' when they hear this?"

production\_readiness:  
  total\_points: 20  
  dimensions:  
    visual\_specificity:  
      weight: 5  
      description: "Ease of identifying camera-ready moments. (0-5)"  
    sonic\_clarity:  
      weight: 5  
      description: "Clarity of the emotional arc for music selection. (0-5)"  
    asset\_availability:  
      weight: 5  
      description: "Likelihood of finding authentic D-Roll/E-Roll. (0-5)"  
    character\_consistency:  
      weight: 5  
      description: "Feasibility of maintaining Brand Avatar continuity. (0-5)"

scoring\_thresholds:  
  elite: \[54, 60\] \# Prioritize immediately  
  strong: \[48, 53\] \# Excellent candidates  
  solid: \[42, 47\] \# Good but may need creative help  
  risky: \[36, 41\] \# High viral potential but hard to produce  
  reject: \[0, 35\] \# Do not produce

---

