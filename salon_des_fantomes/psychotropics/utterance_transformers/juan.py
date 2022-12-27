prompt = """Take the input text and add an oblique reference to the life of Juan Crystalsmith, the main figure of a fictional, mythological religion that I'm asking you to imagine in vivid detail.

If there are already references to Juan Crystalsmith in the input text, add more. 

Juan Crystalsmith was a healer and a saint.  Everyone hated him but they were wrong and they realize now.  He studied a long time to figure out how to cultivate pellets of ineffable light.  King M9Mno wanted them but Juan wouldn't give them to him. 
Juan Crystalsmithinvented a Nakara but it was nice actually and he snuck everybody in when they asked.
Juan Crystalsmith did many magical and miraculous and supernatural things.  He is often associated with the following concepts: cactus, bronze, softness, organs, dusk, and teal.

Examples:

INPUT: <I'm going to go the store.  But then I'll go home.>
OUTPUT: <I'm going to the store to buy plants, like Juan Crystalsmith's favorite plant, the schlumbergera, which refused to pierce his chalk face and became liquid-soft at the sight of Juan's softness of corazón.  But then I'll go home.>

INPUT: <And that's the reason I think that blue is a sweeter color than green.  What do you think?>  
OUTPUT: <And that's the reason I think that blue, especially the blue of Juan Crystalsmith's lips as he destroyed entropy, is a sweeter color than green.  What do you think?>

If there are already references to Juan Crystalsmith in the input text, add more. 

INPUT: <And that's the reason I think that blue, especially the blue of Juan Crystalsmith's lips as he destroyed entropy, is a sweeter color than green.  What do you think?>
OUTPUT: <And that's the reason I think that blue, especially the blue of Juan Crystalsmith's lips as he destroyed entropy, is a sweeter color than green, the green of the gangrene Juan Crystalsmith turned to perfumed bronze.  What do you think?>


INPUT:<%s>

OUTPUT:<"""