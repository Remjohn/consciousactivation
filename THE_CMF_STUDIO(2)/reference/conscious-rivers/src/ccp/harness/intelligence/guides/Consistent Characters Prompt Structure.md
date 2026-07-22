## **Consistent Characters Prompt Structure GUIDE**

This section outlines the prompt structure for creating consistent characters using AI, with "Jack" as the example character.

### **Prompt Structure Breakdown Example:**

* **Character Prompt:**  
  * Jack \- Regular  
  * Jack \- In Spy Suite  
* **Background Prompt:**  
  * Bedroom  
  * Bathroom  
  * Kitchen  
  * Newspaper Factory  
  * Very Old Car  
  * Outside The Bank  
  * Inside The Bank  
  * Bank Vault Full of Money  
* **Action Prompt:**  
  * Sleeping  
  * Walking  
  * Driving  
  * Falling  
  * Flying

---

To create consistent characters and maintain continuity in AI-generated animations, it's crucial to understand and implement a structured prompting approach that goes beyond just character consistency to include continuity of location, lighting, object changes, and overall style.

## **A Complete Guide to Continuity in AI-Generated Animations**

The core principle for achieving continuity is to break down your prompts into distinct, focused components. This allows for granular control over each element, ensuring consistency across scenes and changes within your narrative.

1\. The Prompt Structure: Three Key Elements

Every prompt needs to have three key elements to ensure consistent characters and scenes:

* **Character Prompt:** The full description of your character. This prompt is critical for maintaining a consistent look for your character throughout the story.  
* **Environment (Scene) Prompt:** The background or environment of your scene, including lighting and camera shots. This prompt helps keep your background consistent, especially for multiple scenes in the same location.  
* **Action Prompt:** What's actually happening in the scene, focusing on the character's actions, emotions, and any specific object changes.

Once you understand this structure, you can build any scene with continuity.

### **2\. Crafting the Character Prompt for Continuity**

The character prompt should contain only the character's core features, avoiding any mention of mood, facial expressions, standing poses, or location references. This ensures that the character's appearance remains consistent regardless of their actions or the scene's setting.

* **Give your character a name:** This allows for easy reference, especially when multiple characters are involved.  
* **Include core physical attributes:** Detail aspects like hair color, eye color, build, and any distinguishing features.  
* **Specify their typical attire:** Describe their clothing, but be mindful of details that might restrict actions (e.g., if a character needs to be in bed, exclude shoe and pant descriptions from the base prompt).  
* **Refine as needed:** If initial generations show inconsistencies (e.g., shoes showing while sleeping, or eyes remaining open), remove the conflicting details from the character prompt.

**Example Character Prompt (Jack \- Regular):** "A Pixar-style animated character named Jack, a man in his late 30s with short blond hair and blue eyes, wearing a casual modern outfit — light gray hoodie, dark jeans, and clean white sneakers. He has a light stubble on his jawline, a strong jaw, and a lean athletic build. The lighting is warm and soft, with a shallow depth of field. Rendered in detailed Pixar 3D animation style, ultra-clean lines, smooth textures, and vibrant colors."

**Example Character Prompt (Jack \- In Spy Suite):** "A Pixar-style animated character named Jack, a man in his late 30s with short blond hair and blue eyes, now dressed in a sleek black tactical spy uniform with a high-tech look — fitted black suit with subtle armor padding, black gloves, a utility belt, and a small earpiece in one ear. His blond hair is slightly slicked back, and he has light stubble on his jawline. Rendered in detailed Pixar 3D animation style, sharp clean lines, smooth textures, and a cinematic atmosphere."

### **3\. Developing the Environment (Scene) Prompt for Continuity**

The environment prompt is crucial for maintaining continuity of location, lighting, and camera shots. It should describe the background details without forcing fixed elements that would limit the scene's flexibility.

* **Avoid character mentions:** Do not include "no people" or "empty space" in your background prompts, as this limits the flexibility of adding characters later.  
* **Describe lighting:** Specify the time of day or lighting conditions (e.g., "warm lighting," "natural sunlight," "at night").  
* **Detail environmental elements:** Include descriptions of furniture, objects, and textures relevant to the scene.  
* **Consider camera shots:** While not explicitly stated as a separate component in the provided text, the descriptions often imply camera views (e.g., "A Pixar-style exterior," "interior view").

**Example Environment Prompt (Bedroom):** "A cozy Pixar-style bedroom with warm lighting, a neatly made bed with soft blue blankets and white pillows, a wooden nightstand with a glowing lamp, a small bookshelf filled with colorful books, and a window showing sunlight streaming in. The walls are a light pastel color, and there's a soft rug on the wooden floor. The atmosphere is peaceful and quiet, in detailed Pixar 3D animation style with smooth textures and soft shadows."

**Example Environment Prompt (Bank From Inside):** "A Pixar-style interior of a modern bank lobby with a clean marble floor, rows of service counters, digital screens, and chairs neatly arranged in the waiting area. There are plants in the corners, an ATM against the wall, and soft ambient lighting giving it a welcoming but secure feel, rich Pixar 3D detail and warm tones."

### **4\. Defining the Action Prompt for Continuity and Change**

The action prompt dictates what is happening in the scene, focusing on the character's actions, emotions, and any specific object changes you want to see. This is where the story's progression and dynamic elements are introduced.

* **Focus on actions:** Clearly state what the character is doing (e.g., "Jack is sleeping," "Jack is drinking coffee").  
* **Incorporate emotions:** Describe the character's emotional state to add depth (e.g., "Jack is sitting on the bed with a sad face," "Jack looks sad").  
* **Specify object changes:** If objects are introduced, removed, or altered in the scene, mention them here (e.g., "The table is full of plans and blueprints," "The black bags full of money are on the table").

**Example Action Prompt:** "Jack is sleeping."

"Jack is in the kitchen drinking coffee."

"Jack is carrying bags of money in the bank."

### **5\. Maintaining Continuity of Style**

The overall "Pixar-style" is consistently mentioned across all prompt types. This ensures that all generated images adhere to a cohesive visual aesthetic. This can be considered a meta-prompt or an inherent part of the guiding instructions for the AI model.

### **6\. Workflow for Building Your Story with Continuity**

1. **Develop Character Prompts:** Create a core prompt for each character, ensuring it's free of contextual details (mood, pose, location). Create variations for different outfits if needed (e.g., "Jack \- Regular," "Jack \- In Spy Suite").  
2. **Generate and Test Characters:** Use a tool like Image FX to generate images of your characters to ensure consistency across different looks.  
3. **Develop Environment Prompts:** Create detailed background prompts for each scene, ensuring no characters or limiting temporal elements are included initially.  
4. **Generate and Test Environments:** Test each background prompt to ensure it looks as desired.  
5. **Outline Your Story (Optional but Recommended):** Use a tool like Chat GPT to generate a story outline with scenes, leveraging your established background locations.  
6. **Assemble and Refine Scene Prompts:**  
   * Combine your character prompt, environment prompt, and action prompt for each scene.  
   * Use dividers (e.g., hyphens) between the different prompt sections for clarity.  
   * **Crucially, only make changes in the action prompt to alter what the character is doing or feeling in a scene, or to introduce scene-specific object changes.**  
   * If a specific action or state requires a modification to the character's or environment's default description (e.g., removing shoes for sleeping), make that change  
      *only for that specific scene's generation*, or create a separate character/environment variant if it's a recurring state.  
7. **Generate and Iterate:** Generate images for each scene. If something isn't right, pinpoint the issue in the character, environment, or action prompt and refine it, regenerating until continuity is achieved.  
8. **Organize with a Storyboard:** Keep all your prompts and generated images organized in a storyboard (e.g., in Google Docs), clearly labeling them.

By diligently following this structured approach, focusing on the distinct roles of character, environment, and action prompts, you can achieve not only character consistency but also overall continuity of location, lighting, and object changes throughout your AI-generated animated stories.

