import json
import random

random.seed(42)

TOPICS = {
    "networking": {
        "concepts": {
            "tcp": {
                "base": "TCP (Transmission Control Protocol) is a connection-oriented transport protocol that provides reliable, ordered, and error-checked delivery of data between applications.",
                "how_it_works": "It works by establishing a 3-way handshake (SYN, SYN-ACK, ACK) before transmitting data. It breaks data into packets, numbers them, and uses acknowledgments to ensure no data is lost.",
                "why_important": "TCP is crucial because it guarantees that data arrives complete and in the correct order, which is essential for services where data integrity matters.",
                "applications": "It is widely used in web browsing (HTTP/HTTPS), file transfer (FTP), and email systems (SMTP/IMAP).",
                "limitations": "Due to its error-correction and handshake overhead, it has higher latency compared to UDP and is not ideal for real-time streaming.",
                "example": "For example, when downloading a file, TCP ensures that every single block of the file is received error-free; if a block is lost, it requests a retransmission."
            },
            "udp": {
                "base": "UDP (User Datagram Protocol) is a lightweight, connectionless transport protocol that sends packets without establishing a formal connection.",
                "how_it_works": "It operates by sending independent packets (datagrams) directly to the destination without tracking whether they arrive or checking their order.",
                "why_important": "It is important because it minimizes transmission delay and overhead, making it ideal for time-sensitive applications.",
                "applications": "Commonly used in video streaming, online gaming, DNS queries, and Voice over IP (VoIP).",
                "limitations": "It does not guarantee packet delivery, packet ordering, or recovery from data loss.",
                "example": "For example, in a live video call, losing a few frames (UDP) is acceptable to keep the video running in real-time, whereas waiting for retransmissions would cause lag."
            },
            "ip": {
                "base": "IP (Internet Protocol) is the principal routing protocol used to deliver packets across network boundaries.",
                "how_it_works": "It works by adding IP headers containing source and destination IP addresses to packets, allowing routers to forward them step-by-step toward their destination.",
                "why_important": "Without IP, devices on different networks would not have a standardized way to identify each other or route data globally.",
                "applications": "It forms the foundation of the global Internet and local networks, using IPv4 or IPv6 addressing.",
                "limitations": "IP is a best-effort, connectionless protocol; it does not guarantee delivery or handle error recovery (which is why TCP is run on top of it).",
                "example": "For instance, an IP address acts like a physical mailing address, guiding routers on how to deliver data packets to the correct device."
            },
            "dns": {
                "base": "DNS (Domain Name System) is the internet's directory service that translates human-readable names into IP addresses.",
                "how_it_works": "It queries a hierarchy of DNS servers (Root, TLD, and Authoritative) to resolve a domain name like 'google.com' into an IP address.",
                "why_important": "It eliminates the need for users to memorize complex numerical IP addresses to access websites.",
                "applications": "Used every time you type a URL in a browser, send an email, or access any internet service by name.",
                "limitations": "DNS resolution can add latency to the initial connection, and it is vulnerable to security threats like spoofing and hijacking if not secured with DNSSEC.",
                "example": "For example, typing 'example.com' triggers a DNS request that returns its server IP (e.g., 93.184.216.34) so your browser can connect."
            },
            "http": {
                "base": "HTTP (Hypertext Transfer Protocol) is an application-layer protocol used to request and transmit web resources.",
                "how_it_works": "It uses a request-response model where a client (browser) sends a request (GET, POST) and the server returns a response with status codes and content.",
                "why_important": "It serves as the foundation of data communication for the World Wide Web.",
                "applications": "Used for loading web pages, fetching API data, and transferring files over the web.",
                "limitations": "HTTP transmits data in clear text, making it vulnerable to eavesdropping and tampering by attackers.",
                "example": "For instance, when you click a link, your browser sends an 'HTTP GET' request to the server, which responds with the HTML page."
            },
            "https": {
                "base": "HTTPS (Hypertext Transfer Protocol Secure) is an encrypted version of HTTP that secures communication over computer networks.",
                "how_it_works": "It encrypts standard HTTP traffic using Transport Layer Security (TLS/SSL) to protect data in transit.",
                "why_important": "It prevents unauthorized eavesdropping, data interception, and tampering of sensitive user information.",
                "applications": "Mandatory for online banking, e-commerce, login portals, and modern secure web browsing.",
                "limitations": "Requires SSL certificate management and introduces a minor computational overhead for encryption/decryption handshakes.",
                "example": "For example, when logging into a website via HTTPS, your password is encrypted before leaving your computer, so attackers cannot read it."
            },
            "router": {
                "base": "A router is a physical or virtual network appliance that routes data packets between different networks.",
                "how_it_works": "It examines destination IP addresses in incoming packets and uses its routing table to forward them along the most efficient path.",
                "why_important": "It acts as the gateway between local area networks (LANs) and the global internet (WAN).",
                "applications": "Used in home networks, data centers, and ISP infrastructures to connect separate network segments.",
                "limitations": "Can become a single point of failure if not configured with redundancy, and can cause packet drops if congested.",
                "example": "For instance, your home router connects your local devices (phones, laptops) to the internet service provider's network."
            },
            "switch": {
                "base": "A network switch is a hardware device that connects devices within a single Local Area Network (LAN).",
                "how_it_works": "It uses MAC addresses to forward data frames only to the specific physical port connected to the destination device.",
                "why_important": "It increases network efficiency and reduces packet collisions compared to older hubs by isolating traffic.",
                "applications": "Used to build office networks, school computer labs, and connect server racks in data centers.",
                "limitations": "Operating at Layer 2 (Data Link), standard switches cannot route data between different logical networks without a router.",
                "example": "For example, in a local network, a switch ensures a print job sent from Computer A goes directly to the Printer, not to all computers."
            },
            "firewall": {
                "base": "A firewall is a security device or software that filters incoming and outgoing network traffic.",
                "how_it_works": "It analyzes network packets and permits or blocks them based on a set of defined security rules (e.g., port blocking, IP inspection).",
                "why_important": "It acts as a barrier between a trusted internal network and untrusted external networks like the internet.",
                "applications": "Deployed at network perimeters and on individual hosts to block unauthorized access and malicious activity.",
                "limitations": "Can cause legitimate traffic to be blocked if misconfigured, and cannot stop attacks that bypass it (e.g., social engineering).",
                "example": "For instance, a firewall can block external incoming connection requests on port 22 (SSH) to protect local servers."
            },
            "nat": {
                "base": "NAT (Network Address Translation) is a technique used to map multiple private IP addresses to a single public IP address.",
                "how_it_works": "It modifies the source IP address in the packet header of outgoing traffic and maintains a translation table to route replies back.",
                "why_important": "It slows down the exhaustion of IPv4 addresses and hides internal network structures from the outside world.",
                "applications": "Used by almost all home and corporate routers to connect internal private networks to the public internet.",
                "limitations": "It complicates end-to-end communication, breaks certain peer-to-peer protocols, and adds processing latency.",
                "example": "For example, all devices in your home use private IPs like 192.168.1.X, but to websites, they all appear to use your router's single public IP."
            }
        }
    },
    "machine_learning": {
        "concepts": {
            "machine learning": {
                "base": "Machine learning is a field of artificial intelligence focused on building systems that learn from data to improve their performance automatically.",
                "how_it_works": "It works by feeding large datasets into algorithms that adjust internal mathematical weights to identify patterns and make predictions.",
                "why_important": "It enables computer systems to automate decision-making in complex environments without explicit manual programming.",
                "applications": "Used in recommendation engines, fraud detection, predictive modeling, and spam filtering.",
                "limitations": "Requires massive amounts of clean training data and can inherit biases present in the input dataset.",
                "example": "For example, a machine learning model can learn to identify spam emails by analyzing thousands of emails labeled as spam or inbox."
            },
            "supervised learning": {
                "base": "Supervised learning is a machine learning paradigm where the model is trained on labeled data.",
                "how_it_works": "The algorithm compares its predictions to the correct target labels, calculates the error, and adjusts its parameters to minimize it.",
                "why_important": "It allows models to learn mapped functions and generalize predictions to new, unseen inputs.",
                "applications": "Commonly used for classification tasks (e.g., image tagging) and regression tasks (e.g., predicting house prices).",
                "limitations": "Acquiring high-quality labeled datasets is often expensive, time-consuming, and prone to human labeling errors.",
                "example": "For instance, teaching a model to recognize cars by showing it thousands of photos labeled 'car' or 'not a car'."
            },
            "unsupervised learning": {
                "base": "Unsupervised learning is a machine learning technique where models find hidden structures in unlabeled data.",
                "how_it_works": "The model groups data based on inherent similarities or statistical features without any explicit output target guidance.",
                "why_important": "It helps discover unknown patterns, customer segments, and structural insights from raw data.",
                "applications": "Used for customer segmentation, anomaly detection, dimensionality reduction, and recommendation systems.",
                "limitations": "Evaluating the quality of the output is difficult because there are no ground-truth labels to compare against.",
                "example": "For example, grouping online shoppers into clusters based on their purchasing habits without predefining the categories."
            },
            "reinforcement learning": {
                "base": "Reinforcement learning is an agent-based machine learning paradigm where learning occurs through trial and error.",
                "how_it_works": "An agent interacts with an environment, takes actions, and receives feedback in the form of rewards or penalties to optimize a strategy.",
                "why_important": "It allows systems to learn optimal behaviors and sequential decision-making in dynamic environments.",
                "applications": "Used in autonomous driving, game playing (like AlphaGo), robotics control, and algorithmic trading.",
                "limitations": "Training can be extremely sample-inefficient, computationally expensive, and unstable.",
                "example": "For instance, training a virtual car to drive by giving it positive points for staying in the lane and negative points for crashing."
            },
            "overfitting": {
                "base": "Overfitting is a modeling error that occurs when a machine learning model performs exceptionally well on training data but poorly on test data.",
                "how_it_works": "It happens when the model learns the noise and specific details of the training set rather than the general underlying patterns.",
                "why_important": "Understanding overfitting is critical for building models that generalize well to real-world, unseen data.",
                "applications": "Monitored closely during model training across all ML tasks to ensure robust predictions.",
                "limitations": "Restricts model usability; an overfitted model is practically useless in production.",
                "example": "For example, if a model memorizes the exact training questions for an exam, it will fail when asked slightly modified questions."
            },
            "underfitting": {
                "base": "Underfitting occurs when a machine learning model is too simple to capture the underlying structure of the data.",
                "how_it_works": "It happens when the model lacks capacity, has too few parameters, or is trained for too short a time, leaving it unable to learn the pattern.",
                "why_important": "Detecting underfitting helps developers know when to increase model complexity or gather better features.",
                "applications": "Addressed during the initial phases of model selection and training optimization.",
                "limitations": "Leads to poor accuracy on both the training dataset and new data.",
                "example": "For example, trying to predict complex housing prices using only a simple straight line (linear regression) based on square footage."
            },
            "feature engineering": {
                "base": "Feature engineering is the process of selecting, transforming, and creating input variables from raw data to improve model training.",
                "how_it_works": "It involves techniques like normalization, one-hot encoding, extracting date parts, or creating interaction terms.",
                "why_important": "Good features allow simple models to perform better and make it easier for algorithms to find patterns.",
                "applications": "A vital step in the data preparation phase of any machine learning pipeline.",
                "limitations": "Can be highly domain-specific, time-consuming, and can accidentally introduce data leakage if not done carefully.",
                "example": "For instance, turning a raw timestamp string into 'day of the week' and 'hour of day' to help a traffic prediction model."
            },
            "training dataset": {
                "base": "A training dataset is the primary set of examples used to teach a machine learning model.",
                "how_it_works": "The model reads this data, makes predictions, calculates loss, and updates its weights iteratively during training.",
                "why_important": "The quality, diversity, and volume of the training dataset directly determine the final model's capabilities.",
                "applications": "Used during the fitting phase of models in supervised, unsupervised, and deep learning.",
                "limitations": "If the training dataset is biased or incomplete, the model will produce biased or inaccurate predictions.",
                "example": "For example, using a collection of 10,000 labeled cat and dog photos to train an image classification model."
            },
            "validation set": {
                "base": "A validation set is a distinct subset of data used to tune hyperparameters and prevent overfitting during development.",
                "how_it_works": "Developers train the model on the training set, test it on the validation set, and adjust hyperparameter configurations accordingly.",
                "why_important": "It provides an unbiased evaluation of a model's performance while tuning its parameters.",
                "applications": "Used extensively in model selection, network architecture design, and hyperparameter tuning.",
                "limitations": "If the validation set is too small, performance estimates can be noisy and misleading.",
                "example": "For instance, trying different learning rates on your model and choosing the one that yields the lowest error on the validation split."
            },
            "test set": {
                "base": "A test set is an independent dataset used to assess the final performance and generalization of a fully trained model.",
                "how_it_works": "It is kept completely hidden from the model during training and validation, and is only evaluated once at the very end.",
                "why_important": "It mimics real-world unseen data, giving a true measure of the model's accuracy.",
                "applications": "Used as the final benchmark before deploying a machine learning model into production.",
                "limitations": "Must never be used to make decisions during model training; doing so causes data leakage and invalidates test results.",
                "example": "For example, evaluating your final model on 1,000 secret images that the model has never encountered to verify its real-world accuracy."
            }
        }
    },
    # بقیه تاپیک‌ها به همین ترتیب برای تنوع ساختاری دسته‌بندی می‌شوند...
    "deep_learning": {
        "concepts": {
            "deep learning": {
                "base": "Deep learning is a specialized subfield of machine learning that utilizes multi-layered artificial neural networks.",
                "how_it_works": "It automatically learns hierarchical features from raw data by passing inputs through multiple hidden layers of computational nodes.",
                "why_important": "It eliminates the need for manual feature engineering by learning features directly from data.",
                "applications": "Powering advanced systems like autonomous driving, face recognition, and large language models (LLMs).",
                "limitations": "Requires massive computational resources (GPUs) and a vast amount of training data to prevent overfitting.",
                "example": "For example, in image recognition, lower layers detect edges, middle layers detect shapes, and high layers detect complete objects."
            },
            "neural network": {
                "base": "An artificial neural network is a computational model inspired by the biological structure of the human brain.",
                "how_it_works": "It consists of layers of nodes (neurons) connected by weights. Inputs are processed through activation functions to produce outputs.",
                "why_important": "It acts as the primary building block for all deep learning models, capable of approximating any complex mathematical function.",
                "applications": "Used across predictive analytics, classification, translation, and generative tasks.",
                "limitations": "Often functions as a 'black box', making it difficult to explain why the model made a specific decision.",
                "example": "For instance, a network takes pixel values as input, passes them through weighted connections, and outputs the probability of the image containing a dog."
            },
            "cnn": {
                "base": "A CNN (Convolutional Neural Network) is a deep learning architecture designed for processing grid-structured data like images.",
                "how_it_works": "It applies convolutional filters to scan local areas of an input, preserving spatial relationships and extracting local features.",
                "why_important": "It is parameter-efficient because it uses weight sharing, making it highly effective for computer vision tasks.",
                "applications": "Used in image classification, object detection, medical image analysis, and video processing.",
                "limitations": "Struggles with understanding scale and rotation changes unless explicitly trained with augmented data.",
                "example": "For example, a CNN uses filters to detect horizontal or vertical edges in an image of a handwritten digit."
            },
            "rnn": {
                "base": "An RNN (Recurrent Neural Network) is a class of neural networks tailored for sequential or time-series data.",
                "how_it_works": "It features internal loops that allow information to persist, using the output of a previous step as input to the next step.",
                "why_important": "It handles inputs of variable lengths and processes sequential dependencies over time.",
                "applications": "Used in speech recognition, time-series forecasting, and language translation.",
                "limitations": "Suffers from the vanishing gradient problem, making it difficult to remember long-range dependencies.",
                "example": "For instance, predicting the next word in the sentence 'The sky is ___' based on the contextual sequence."
            },
            "lstm": {
                "base": "LSTM (Long Short-Term Memory) is an advanced RNN architecture designed to learn long-term dependencies in sequence data.",
                "how_it_works": "It introduces a cell state and three control gates (input, forget, and output gates) to selectively regulate the flow of information.",
                "why_important": "It successfully mitigates the vanishing gradient problem, enabling the network to remember information over long steps.",
                "applications": "Commonly used in text generation, stock price prediction, and speech synthesis.",
                "limitations": "More complex and slower to train than standard RNNs due to its internal gating mechanisms.",
                "example": "For example, remembering the gender of a subject mentioned early in a paragraph to ensure grammatical consistency later."
            },
            "attention": {
                "base": "Attention is a mechanism that allows neural networks to focus selectively on specific parts of the input sequence.",
                "how_it_works": "It calculates alignment scores between different tokens, assigning higher mathematical weights to parts that are semantically relevant.",
                "why_important": "It removes the bottleneck of representing an entire sequence with a single fixed-length vector.",
                "applications": "Forms the core of modern machine translation and generative AI architectures.",
                "limitations": "Significantly increases memory usage, as calculating pairwise attention weights scales quadratically with sequence length.",
                "example": "For instance, when translating 'the white house' to French, attention links 'white' to 'blanc' and 'house' to 'maison'."
            },
            "transformer": {
                "base": "The Transformer is a neural network architecture based entirely on self-attention mechanisms.",
                "how_it_works": "It processes sequence inputs in parallel rather than sequentially, utilizing multi-head self-attention and positional encodings.",
                "why_important": "It allows much faster training on GPUs and handles very long contextual dependencies efficiently.",
                "applications": "The underlying architecture behind state-of-the-art models like GPT, BERT, Claude, and LLaMA.",
                "limitations": "Requires massive datasets and high computational power to train from scratch.",
                "example": "For example, a Transformer can process an entire page of text simultaneously to predict the next word in a sentence."
            },
            "self-attention": {
                "base": "Self-attention is an attention mechanism relating different positions of a single sequence to compute its representation.",
                "how_it_works": "It calculates Query, Key, and Value vectors for each token to determine how much attention each word should pay to every other word.",
                "why_important": "It enables tokens to capture contextual meaning relative to all other words in the same sentence.",
                "applications": "Used inside Transformer blocks to understand sentence structure and semantics.",
                "limitations": "Requires a quadratic amount of memory relative to the sequence length.",
                "example": "For example, in 'The bank of the river', self-attention links 'bank' with 'river' to understand it refers to land, not a financial institution."
            },
            "embedding": {
                "base": "An embedding is a dense vector representation of data that captures semantic meaning in a continuous vector space.",
                "how_it_works": "It maps high-dimensional discrete tokens (like words) to low-dimensional vectors where geometrically close vectors represent semantically similar items.",
                "why_important": "It allows algorithms to perform mathematical operations on text while preserving semantic relationships.",
                "applications": "Crucial for text classification, semantic search, recommender systems, and language models.",
                "limitations": "Static embeddings (like Word2Vec) assign the same vector to homonyms, ignoring the specific sentence context.",
                "example": "For example, the vectors for 'king' and 'queen' will be close to each other in the vector space due to their semantic similarities."
            },
            "fine-tuning": {
                "base": "Fine-tuning is the process of taking a pre-trained model and training it further on a smaller, domain-specific dataset.",
                "how_it_works": "The model starts with pre-learned weights and updates them slightly on the new dataset using a low learning rate.",
                "why_important": "It allows developers to build high-performing specialized models without the high cost of training from scratch.",
                "applications": "Used to adapt general language models for specific tasks like customer support bots or legal document analysis.",
                "limitations": "Can lead to 'catastrophic forgetting' where the model loses some of its original general capabilities.",
                "example": "For instance, taking a general model trained on the internet and fine-tuning it on medical research papers to answer health queries."
            }
        }
    },
    "nlp": {
        "concepts": {
            "natural language processing": {
                "base": "Natural Language Processing (NLP) is a branch of AI that bridges the gap between human communication and computer understanding.",
                "how_it_works": "It applies linguistic models, statistical algorithms, and deep learning to parse, analyze, and generate human languages.",
                "why_important": "It enables machines to process massive amounts of unstructured text data and interact naturally with humans.",
                "applications": "Powering search engines, chatbots, automated translation, voice assistants, and sentiment monitoring.",
                "limitations": "Human language is highly ambiguous, context-dependent, and full of sarcasm or idiom, which are hard for models to interpret.",
                "example": "For example, NLP helps a search engine understand that 'apple store' refers to the technology company, not a fruit shop."
            },
            "tokenization": {
                "base": "Tokenization is the process of breaking raw text down into smaller, manageable pieces called tokens.",
                "how_it_works": "It splits sentences based on spaces, punctuation, or subword patterns using algorithms like Byte-Pair Encoding (BPE).",
                "why_important": "It is the essential first step in NLP, preparing raw text for numerical vectorization and model ingestion.",
                "applications": "Used in text pre-processing pipelines for search indexes, classifiers, and transformer models.",
                "limitations": "Different languages require different tokenization rules; segmenting languages without clear word boundaries (like Chinese) is complex.",
                "example": "For instance, tokenizing the sentence 'I love AI' into three distinct word tokens: ['I', 'love', 'AI']."
            },
            "stemming": {
                "base": "Stemming is a crude text normalization technique that chops off word suffixes to reduce them to their base form.",
                "how_it_works": "It uses crude heuristic rules (e.g., Porter Stemmer) to strip endings like '-ing', '-ed', or '-s' without analyzing context.",
                "why_important": "It maps different grammatical variations of a word to a single index, reducing vocabulary size.",
                "applications": "Mainly used in search engine indexing and basic text classification setups.",
                "limitations": "Often leads to non-dictionary words (over-stemming) and ignores word meanings (under-stemming).",
                "example": "For example, stemming the words 'running', 'runs', and 'ran' might result in the root form 'run', but 'universal' might stem to 'univers'."
            },
            "lemmatization": {
                "base": "Lemmatization is a advanced linguistic process that returns a word to its dictionary root form (lemma).",
                "how_it_works": "It uses a dictionary and part-of-speech (POS) tagging to analyze the grammatical context and resolve the base form.",
                "why_important": "It is much more precise than stemming, preserving the proper semantic dictionary representation of words.",
                "applications": "Used in text preprocessing for high-quality translation, summarization, and information retrieval.",
                "limitations": "Requires significant computational resources and linguistic lookup databases compared to simple stemming.",
                "example": "For instance, lemmatizing the word 'better' returns 'good', whereas a stemmer might output 'bett' or leave it unchanged."
            },
            "named entity recognition": {
                "base": "Named Entity Recognition (NER) is an NLP task that identifies and classifies key entities in text.",
                "how_it_works": "It uses sequence labeling models to locate spans of text and categorize them into predefined classes like names, dates, or locations.",
                "why_important": "It helps structure unstructured text, allowing databases to automatically extract relationships and facts.",
                "applications": "Used to extract information from news articles, classify support tickets, and build knowledge graphs.",
                "limitations": "Struggles with ambiguous names (e.g., distinguishing whether 'Apple' refers to the fruit or the tech company in a complex sentence).",
                "example": "For instance, processing 'Elon Musk visited Paris in 2023' extracts Elon Musk (Person), Paris (Location), and 2023 (Date)."
            },
            "sentiment analysis": {
                "base": "Sentiment analysis is the computational task of identifying the emotional tone expressed in a text.",
                "how_it_works": "It analyzes linguistic features or uses deep learning models to classify text into sentiments like positive, negative, or neutral.",
                "why_important": "It allows organizations to automatically track customer satisfaction and public opinion at scale.",
                "applications": "Used for monitoring social media mentions, tracking product reviews, and analyzing survey responses.",
                "limitations": "Struggles to accurately identify sarcasm, double negatives, or highly nuanced feedback.",
                "example": "For example, analyzing a product review 'The battery is terrible!' classifies the customer sentiment as negative."
            },
            "language model": {
                "base": "A language model is a statistical or neural model trained to estimate the probability of sequences of words.",
                "how_it_works": "It calculates the likelihood of a word sequence occurring, allowing it to predict the most probable next word in a sequence.",
                "why_important": "It is the foundational technology behind text generation, auto-completion, translation, and virtual assistants.",
                "applications": "Forms the basis of search auto-complete, predictive keyboards, and modern conversational bots.",
                "limitations": "Can hallucinate incorrect facts because it models word probabilities rather than absolute truth.",
                "example": "For instance, given 'The cat sat on the ___', the model predicts 'mat' as a highly probable next word."
            },
            "bert": {
                "base": "BERT (Bidirectional Encoder Representations from Transformers) is a Transformer-based model designed to pre-train language representations.",
                "how_it_works": "It uses a masked language model objective, reading sentences bidirectionally (left-to-right and right-to-left) to capture deep context.",
                "why_important": "It revolutionized NLP by enabling models to understand the context of a word based on its surroundings.",
                "applications": "Powers Google Search queries, question answering systems, and text classification tasks.",
                "limitations": "It is an encoder-only model, meaning it is excellent at understanding text but not suited for generating new text.",
                "example": "For example, BERT can distinguish the meaning of 'bank' in 'river bank' versus 'money bank' by looking at surrounding words."
            },
            "gpt": {
                "base": "GPT (Generative Pre-trained Transformer) is a family of decoder-only transformer language models designed for text generation.",
                "how_it_works": "It uses autoregressive generation, predicting the next token in a sequence based on all previous tokens it has generated.",
                "why_important": "It excels at writing coherent, human-like text, answering questions, and writing code.",
                "applications": "Powers conversational AI like ChatGPT, code generation tools, creative writing assistants, and translation tasks.",
                "limitations": "Requires strict guardrails to prevent generating toxic content or plausible-sounding but false information.",
                "example": "For example, asking GPT to write a poem about autumn results in it generating a flowing, contextually appropriate text line-by-line."
            },
            "prompt engineering": {
                "base": "Prompt engineering is the practice of designing and refining inputs to guide the output behavior of generative AI models.",
                "how_it_works": "It involves constructing queries with system instructions, formatting guidelines, and examples (few-shot prompting).",
                "why_important": "It allows developers to control the tone, structure, and accuracy of AI responses without modifying model weights.",
                "applications": "Used to build robust AI agents, specialized API integrations, and prompt templates for chatbots.",
                "limitations": "It is heuristic and can be unstable, as minor changes in prompt phrasing can lead to highly varied outputs.",
                "example": "For instance, adding 'Explain step-by-step for a 10-year-old:' before a question forces the AI to output a simplified explanation."
            }
        }
    },
    "databases": {
        "concepts": {
            "database": {
                "base": "A database is a structured system designed to store, organize, manage, and retrieve data efficiently.",
                "how_it_works": "It uses software called a Database Management System (DBMS) to handle storage engines, file layouts, indexing, and transactional integrity.",
                "why_important": "It provides a persistent, secure, and multi-user storage environment for all software applications.",
                "applications": "Used in banking systems, user profiles, inventory tracking, and logs.",
                "limitations": "Requires careful database administration, hardware scaling, and query tuning to prevent performance degradation.",
                "example": "For example, an online shop uses a database to keep track of user accounts, orders, and products."
            },
            "sql": {
                "base": "SQL (Structured Query Language) is the standard language used to interact with relational databases.",
                "how_it_works": "It uses declarative syntax (SELECT, INSERT, UPDATE, DELETE) to define data manipulation and schema structures.",
                "why_important": "It provides a standardized, powerful way to query complex relationships between tables.",
                "applications": "Used to query systems like PostgreSQL, MySQL, SQL Server, and Oracle.",
                "limitations": "Not natively optimized for hierarchical or highly dynamic, unstructured data schemas.",
                "example": "For instance, running 'SELECT * FROM users WHERE status = \"active\"' queries active users."
            },
            "nosql": {
                "base": "NoSQL refers to non-relational databases designed to store and query unstructured or semi-structured data.",
                "how_it_works": "It uses diverse data models like document, key-value, column-family, or graph stores instead of tables.",
                "why_important": "It offers horizontal scalability, high performance, and schema flexibility for rapid software development.",
                "applications": "Used in real-time analytics, content management, caching, and social networks (MongoDB, Redis, Cassandra).",
                "limitations": "Often sacrifices ACID guarantees in favor of performance and availability (Eventual Consistency).",
                "example": "For example, MongoDB stores user profiles as JSON-like documents, allowing each user to have different fields."
            },
            "indexing": {
                "base": "Indexing is a database performance optimization technique that accelerates query lookup times.",
                "how_it_works": "It creates a separate data structure (like a B-Tree or Hash Index) that maps index keys directly to row disk locations.",
                "why_important": "It prevents expensive sequential scans over millions of rows, returning search results in milliseconds.",
                "applications": "Implemented on columns frequently used in WHERE clauses, JOIN conditions, or ORDER BY statements.",
                "limitations": "Slows down write operations (INSERT, UPDATE, DELETE) because the index structures must be updated.",
                "example": "For instance, an index works like a book index: instead of reading the entire book, you search the index to find the page."
            },
            "normalization": {
                "base": "Normalization is the process of organizing data inside relational databases to reduce redundancy.",
                "how_it_works": "It decomposes tables into smaller relationships using rules called Normal Forms (1NF, 2NF, 3NF).",
                "why_important": "It prevents data anomalies during updates and ensures data consistency across the database.",
                "applications": "Crucial during database design for transactional systems (OLTP).",
                "limitations": "Can lead to complex queries requiring multiple table JOINs, which can degrade read performance.",
                "example": "For example, splitting a customer table so the customer's city address is stored in a separate lookup table."
            },
            "acid": {
                "base": "ACID is a set of properties that guarantee relational database transactions are processed reliably.",
                "how_it_works": "It enforces Atomicity (all or nothing), Consistency (valid state), Isolation (independent transactions), and Durability (permanent changes).",
                "why_important": "It ensures data integrity and prevents corruption, even during system crashes or power failures.",
                "applications": "Mandatory for critical financial transactions, booking systems, and banking operations.",
                "limitations": "Enforcing isolation levels requires locking mechanisms, which can reduce concurrency and write throughput.",
                "example": "For instance, when transferring money, ACID guarantees that money is both deducted from Account A and added to Account B."
            },
            "transaction": {
                "base": "A database transaction is a sequence of read and write operations treated as a single logical unit of work.",
                "how_it_works": "It groups queries between BEGIN and COMMIT statements. If any operation fails, the transaction is rolled back.",
                "why_important": "It prevents partial updates that would leave the database in an inconsistent state.",
                "applications": "Used during multi-step data updates, like checking out a shopping cart and updating inventory.",
                "limitations": "Long-running transactions can block database locks, leading to system timeouts.",
                "example": "For example, booking a flight is a transaction: it reserves the seat, charges the card, and issues the ticket."
            },
            "primary key": {
                "base": "A primary key is a column or set of columns that uniquely identifies each row in a database table.",
                "how_it_works": "It enforces uniqueness and NOT NULL constraints, indexing the column automatically for fast access.",
                "why_important": "It guarantees that every record in a table can be distinctively referenced.",
                "applications": "Found in almost every relational database table to connect related tables.",
                "limitations": "A table can only have one primary key, and changing primary key values after creation is highly discouraged.",
                "example": "For instance, using a unique Auto-Incremented 'User_ID' to identify a specific customer."
            },
            "foreign key": {
                "base": "A foreign key is a column that establishes a link between data in two different database tables.",
                "how_it_works": "It maps a column in a child table to the primary key of a parent table, enforcing referential integrity.",
                "why_important": "It prevents orphan records by restricting actions like deleting parent records without updating child records.",
                "applications": "Used to model relationships like 'One-to-Many' (e.g., one customer having multiple orders).",
                "limitations": "Can add performance overhead during inserts and deletes because the database must verify constraints.",
                "example": "For example, the 'orders' table contains a 'customer_id' foreign key referencing the 'customers' table."
            },
            "vector database": {
                "base": "A vector database is a database optimized for storing and querying high-dimensional vectors (embeddings).",
                "how_it_works": "It indexes vectors using algorithms like HNSW or IVF and performs similarity searches (e.g., Cosine Similarity).",
                "why_important": "It allows AI systems to retrieve contextually similar documents, images, or audios in real-time.",
                "applications": "Powers Retrieval-Augmented Generation (RAG), recommendation systems, and semantic search.",
                "limitations": "Usually does not support standard relational features (like SQL joins) and can be memory-heavy.",
                "example": "For example, searching a vector database for the word 'dog' returns sentences about puppies or canine behaviors."
            }
        }
    },
    "operating_systems": {
        "concepts": {
            "operating system": {
                "base": "An operating system (OS) is system software that manages computer hardware and software resources.",
                "how_it_works": "It controls the CPU, memory, storage devices, and provides a platform for applications to run via API calls.",
                "why_important": "It acts as an intermediary between user applications and the physical computer hardware.",
                "applications": "Runs on everything from personal computers (Windows, macOS) and servers (Linux) to mobile devices (iOS, Android).",
                "limitations": "Binds applications to its specific environment, and OS overhead consumes system RAM and CPU cycles.",
                "example": "For example, Windows manages your system resources so you can run a game and browse the web simultaneously."
            },
            "process": {
                "base": "A process is an active instance of a computer program in execution.",
                "how_it_works": "The OS assigns each process its own isolated memory address space, registers, stack, and file descriptors.",
                "why_important": "Memory isolation between processes prevents a crash in one program from taking down the entire operating system.",
                "applications": "Every running application on a computer (like a browser or text editor) runs as one or more processes.",
                "limitations": "Creating and switching between processes is resource-intensive due to memory context switching.",
                "example": "For instance, running Chrome and Spotify simultaneously creates separate processes with isolated memory."
            },
            "thread": {
                "base": "A thread is the smallest unit of execution within a process, often called a lightweight process.",
                "how_it_works": "Threads within the same process share the process's memory space and resources but have their own call stacks.",
                "why_important": "They allow concurrent tasks within a single program (like playing audio while downloading a file).",
                "applications": "Used heavily in multi-threaded servers, video rendering, and responsive UI applications.",
                "limitations": "Because they share memory, bugs can lead to concurrency issues like race conditions or data corruption.",
                "example": "For example, a web browser uses one thread to render the webpage and another thread to handle user inputs."
            },
            "scheduling": {
                "base": "Scheduling is the OS mechanism that determines which process receives CPU execution time.",
                "how_it_works": "It uses algorithms like Round Robin, Priority Scheduling, or Multi-Level Feedback Queues to manage execution flow.",
                "why_important": "It ensures fair CPU utilization, minimizes latency, and maintains system responsiveness.",
                "applications": "Handled continuously by the OS kernel's scheduler to balance tasks.",
                "limitations": "Poor scheduling designs can cause starvation, where low-priority processes never get CPU time.",
                "example": "For instance, scheduling prevents a heavy background download from freezing your mouse movement."
            },
            "deadlock": {
                "base": "A deadlock is a system state where a set of processes are blocked because each holds a resource the other needs.",
                "how_it_works": "It occurs when four conditions are met: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.",
                "why_important": "Understanding deadlocks allows developers to design resource locking strategies that prevent system freezes.",
                "applications": "Monitored and prevented in databases, multi-threaded applications, and OS kernels.",
                "limitations": "Resolving deadlocks usually requires terminating one of the blocked processes, leading to lost work.",
                "example": "For example, Process A holds Resource 1 and waits for Resource 2; Process B holds Resource 2 and waits for Resource 1."
            },
            "virtual memory": {
                "base": "Virtual memory is a memory management feature that mapping physical RAM addresses to virtual addresses.",
                "how_it_works": "It swaps inactive memory pages out to physical disk storage (swap space) when RAM runs low, bringing them back when needed.",
                "why_important": "It allows computers to run programs that are larger than the physical RAM installed on the machine.",
                "applications": "Implemented in almost all modern consumer and server operating systems.",
                "limitations": "Swapping data to disk (thrashing) is significantly slower than reading directly from physical RAM.",
                "example": "For instance, virtual memory lets you open a 16GB project file on a laptop that only has 8GB of RAM."
            },
            "paging": {
                "base": "Paging is a memory management scheme that eliminates the need for contiguous physical memory allocation.",
                "how_it_works": "The OS divides virtual memory into fixed-size blocks (pages) and maps them to physical frames in RAM using a Page Table.",
                "why_important": "It prevents external memory fragmentation, allowing flexible memory allocation for processes.",
                "applications": "Used directly by the CPU's Memory Management Unit (MMU) and the OS kernel.",
                "limitations": "Can suffer from internal fragmentation if processes use only a small fraction of a allocated page.",
                "example": "For instance, when a program requests memory, the OS allocates pages wherever frames are free in RAM, even if scattered."
            },
            "kernel": {
                "base": "The kernel is the core component of an operating system that has complete control over everything in the system.",
                "how_it_works": "It acts as the bridge between software applications and data processing performed at the hardware level.",
                "why_important": "It manages system resources, handles device drivers, and secures hardware access.",
                "applications": "The fundamental engine of operating systems (e.g., Linux kernel, NT kernel for Windows).",
                "limitations": "A crash in the kernel space is catastrophic, usually resulting in a Blue Screen (BSOD) or complete system panic.",
                "example": "For example, when an app writes a file, the kernel validates permissions and manages the physical hard drive write."
            },
            "system call": {
                "base": "A system call is the programmatic way a user space application requests a service from the OS kernel.",
                "how_it_works": "It triggers a software interrupt, switching the CPU from user mode to privileged kernel mode to execute the operation.",
                "why_important": "It prevents user programs from directly manipulating hardware, ensuring system safety.",
                "applications": "Used for operations like reading/writing files, creating processes, or sending network packets.",
                "limitations": "Swapping between user mode and kernel mode introduces a performance overhead.",
                "example": "For example, when a Python script calls 'open()', it triggers a system call asking the kernel to access the storage."
            },
            "file system": {
                "base": "A file system is the structure and rules used by an OS to organize and retrieve files on a storage device.",
                "how_it_works": "It indexes files, translates logical names to physical disk blocks, and manages directories, metadata, and permissions.",
                "why_important": "Without a file system, a hard drive would be a massive stream of raw bytes with no way to identify files.",
                "applications": "Used to format drives (e.g., NTFS, ext4, APFS, FAT32) for storage compatibility.",
                "limitations": "Different file systems have maximum file size limits and are not natively readable by all operating systems.",
                "example": "For instance, the file system keeps track of where 'report.docx' is physically stored on your SSD."
            }
        }
    },
    "software_engineering": {
        "concepts": {
            "software engineering": {
                "base": "Software engineering is the systematic application of engineering principles to software development.",
                "how_it_works": "It follows structured methodologies (like Agile or Waterfall) covering requirements analysis, design, testing, and maintenance.",
                "why_important": "It ensures that complex software systems are built reliably, within budget, and are easy to maintain.",
                "applications": "Applied across all software development industries and engineering teams.",
                "limitations": "Strict processes can sometimes slow down development and reduce team flexibility if over-engineered.",
                "example": "For example, using design patterns and automated testing pipelines to build a stable online banking application."
            },
            "api": {
                "base": "An API (Application Programming Interface) is a set of protocols and tools that allows different software applications to communicate.",
                "how_it_works": "It exposes specific functions and endpoints that other developers can call without needing to know the internal code logic.",
                "why_important": "It enables integration and modularity, letting programs easily share data and services.",
                "applications": "Used in web services, operating systems, software libraries, and database connectors.",
                "limitations": "API changes can break dependent applications if not properly versioned and documented.",
                "example": "For instance, a weather website uses a weather service API to fetch and display the current temperature."
            },
            "rest api": {
                "base": "A REST API is an architectural style for design web APIs that relies on standard HTTP protocol methods.",
                "how_it_works": "It uses stateless client-server communication, representing resources with URLs and interacting via GET, POST, PUT, and DELETE.",
                "why_important": "Its stateless nature makes it scalable, standard, and highly compatible with web browsers.",
                "applications": "The most common standard for communication in web development and mobile app backends.",
                "limitations": "Can suffer from over-fetching or under-fetching data, requiring multiple round-trips to the server.",
                "example": "For example, sending a GET request to '/api/users/42' to retrieve details for user number 42."
            },
            "microservices": {
                "base": "Microservices is an architectural style where an application is built as a collection of small, independent services.",
                "how_it_works": "Each service runs its own process, manages its own database, and communicates via lightweight protocols like HTTP/REST or gRPC.",
                "why_important": "It allows teams to scale and deploy parts of an application independently without affecting the whole system.",
                "applications": "Used by large platforms like Netflix, Amazon, and Spotify to manage complex, massive applications.",
                "limitations": "Introduces significant complexity in network communication, distributed data management, and monitoring.",
                "example": "For instance, an e-commerce platform has separate services for User Authentication, Payment, and Inventory."
            },
            "version control": {
                "base": "Version control is a system that records changes to files over time so you can recall specific versions later.",
                "how_it_works": "It tracks modifications in code files, logs commit histories, and manages branch mergers.",
                "why_important": "It prevents team members from overwriting each other's code and allows rolling back changes when errors occur.",
                "applications": "Essential for team collaboration in software engineering, document drafting, and configuration management.",
                "limitations": "Requires a learning curve for merge conflict resolution and repository management.",
                "example": "For instance, Git allows multiple developers to work on the same codebase simultaneously without destroying history."
            },
            "git": {
                "base": "Git is a distributed version control system designed to handle everything from small to large projects with speed.",
                "how_it_works": "Every developer has a full copy of the repository history locally, enabling offline work and fast branching/merging.",
                "why_important": "It is the industry standard tool for coordinating programming tasks and code versioning.",
                "applications": "Used in combination with platforms like GitHub, GitLab, and Bitbucket for team collaboration.",
                "limitations": "Its command-line interface can be complex and confusing for beginners.",
                "example": "For example, running 'git commit' saves your local progress, and 'git push' uploads it to share with your team."
            },
            "testing": {
                "base": "Software testing is the process of evaluating code execution to verify it meets specification requirements.",
                "how_it_works": "It executes software using manual methods or automated scripts to detect bugs, security flaws, or performance issues.",
                "why_important": "It ensures code quality, reduces development costs, and prevents bugs from reaching final production users.",
                "applications": "Performed continuously during the development cycle (CI/CD pipelines).",
                "limitations": "Testing can show the presence of bugs but can never prove that a program is completely error-free.",
                "example": "For instance, running automated scripts to check if the checkout button works correctly on different web browsers."
            },
            "unit testing": {
                "base": "Unit testing is a software testing method where individual units of source code are tested in isolation.",
                "how_it_works": "Developers write test cases for specific functions or methods, mocking external dependencies (like databases) to isolate the code.",
                "why_important": "It allows developers to verify that small code modules work correctly before integration.",
                "applications": "A standard practice in modern test-driven development (TDD).",
                "limitations": "Does not catch integration bugs that occur when different modules interact with each other.",
                "example": "For example, writing a test to verify that the function 'add(2, 3)' correctly returns exactly 5."
            },
            "debugging": {
                "base": "Debugging is the analytical process of identifying and resolving bugs or defects in software.",
                "how_it_works": "It involves inspecting logs, setting breakpoints in tools called debuggers, and stepping through code execution.",
                "why_important": "It is necessary to fix unexpected behaviors and crashes in both development and production code.",
                "applications": "Done by developers across all programming environments and software lifecycle phases.",
                "limitations": "Can be extremely time-consuming and difficult if the codebase is poorly structured or lacks logs.",
                "example": "For instance, using print statements or breakpoints to find out why a variable is returning 'None' instead of a list."
            },
            "refactoring": {
                "base": "Refactoring is the process of restructuring existing computer code without changing its external behavior.",
                "how_it_works": "It cleans up code structures, removes duplicates, and improves naming conventions to increase readability and maintainability.",
                "why_important": "It reduces technical debt and makes the codebase easier to extend or modify in the future.",
                "applications": "Regularly performed during code reviews and software maintenance cycles.",
                "limitations": "If not supported by a strong suite of automated tests, refactoring can accidentally introduce new bugs.",
                "example": "For example, breaking a massive 500-line function into five smaller, well-named helper functions."
            }
        }
    },
    "cybersecurity": {
        "concepts": {
            "cybersecurity": {
                "base": "Cybersecurity is the practice of defending computers, servers, networks, and data from malicious attacks.",
                "how_it_works": "It uses a multi-layered defense model spanning network security, application security, host security, and user training.",
                "why_important": "It protects sensitive personal information, proprietary business data, and critical national infrastructure from hackers.",
                "applications": "Implemented across corporate infrastructures, defense departments, and personal devices.",
                "limitations": "Security is a continuous battle; new vulnerabilities are constantly discovered, meaning no system is 100% secure.",
                "example": "For instance, combining encryption, firewalls, and strong password policies to protect user accounts from breaches."
            },
            "encryption": {
                "base": "Encryption is the process of encoding information so that only authorized parties can read it.",
                "how_it_works": "It uses mathematical algorithms and cryptographic keys to convert readable plaintext into unreadable ciphertext.",
                "why_important": "It guarantees data confidentiality, ensuring that intercepted data remains useless to attackers.",
                "applications": "Used in securing web traffic (HTTPS), messaging apps (Signal), and file storage systems.",
                "limitations": "If cryptographic keys are lost, the encrypted data is permanently unrecoverable.",
                "example": "For example, encrypting the message 'Hello' into 'x8$yP' using an encryption algorithm."
            },
            "phishing": {
                "base": "Phishing is a social engineering attack where targets are contacted by email, telephone, or text message.",
                "how_it_works": "Attackers pose as legitimate institutions to lure individuals into providing sensitive data, such as passwords or credit cards.",
                "why_important": "Understanding phishing is key because human error remains the most common entry point for cyber attacks.",
                "applications": "Tackled via email spam filters, domain verification policies, and security awareness training.",
                "limitations": "Technical filters cannot block all phishing attacks, as attackers continuously evolve their social engineering tactics.",
                "example": "For instance, receiving a fake email designed to look like your bank, claiming your account is locked and asking you to log in."
            },
            "malware": {
                "base": "Malware (malicious software) is an umbrella term for any software designed to disrupt, damage, or gain unauthorized access.",
                "how_it_works": "It infects systems through software vulnerabilities, phishing, or malicious downloads, executing unauthorized code.",
                "why_important": "It is the primary tool used by cybercriminals to steal data, hijack resources, or spy on user activity.",
                "applications": "Analyzed by security researchers and blocked using antivirus programs and endpoint detection tools.",
                "limitations": "New, zero-day malware can bypass traditional signature-based security scanners.",
                "example": "For example, a spyware program that quietly records your keystrokes to steal your login credentials."
            },
            "ransomware": {
                "base": "Ransomware is a type of malware that locks and encrypts a victim's files, demanding payment to decrypt them.",
                "how_it_works": "Once inside a network, it silently encrypts target files and deletes system backups, presenting a ransom note.",
                "why_important": "It is one of the most destructive cybersecurity threats, causing massive financial and operational damage.",
                "applications": "Fought with offline backup strategies, system updates, and strict access control lists.",
                "limitations": "Even if the ransom is paid, there is no guarantee that the attackers will provide the decryption key.",
                "example": "For instance, a hospital's database getting encrypted by attackers, stopping all medical systems until a ransom is paid."
            },
            "authentication": {
                "base": "Authentication is the security process of verifying the identity of a user, device, or system.",
                "how_it_works": "It verifies credentials against factors: something you know (password), have (token), or are (fingerprint).",
                "why_important": "It prevents unauthorized users from accessing sensitive systems and accounts.",
                "applications": "Used in login systems, biometric scanners, and smart card readers.",
                "limitations": "Can be bypassed if credentials are weak, stolen via phishing, or if the authentication server is compromised.",
                "example": "For example, typing your password and then entering a code sent to your phone (Multi-Factor Authentication)."
            },
            "authorization": {
                "base": "Authorization is the security process of determining what permissions an authenticated user has.",
                "how_it_works": "It checks user roles and Access Control Lists (ACLs) to permit or deny actions (like read, write, or delete).",
                "why_important": "It ensures that users can only access the resources necessary for their specific roles (Principle of Least Privilege).",
                "applications": "Managed within database configurations, cloud environments, and application routers.",
                "limitations": "Misconfigured permission systems can lead to privilege escalation vulnerabilities.",
                "example": "For instance, allowing an Employee to view their own profile, but only allowing the HR Manager to edit salary fields."
            },
            "hashing": {
                "base": "Hashing is the cryptographic process of turning any input data into a fixed-length string of characters.",
                "how_it_works": "It uses one-way hash functions (like SHA-256) designed so that it is mathematically impossible to reverse the output to find the input.",
                "why_important": "It is critical for securely storing user passwords and verifying file integrity.",
                "applications": "Used in password databases, blockchain technology, and digital signature verifications.",
                "limitations": "Vulnerable to collision attacks if outdated algorithms (like MD5) are used.",
                "example": "For instance, hashing the password '123456' to save 'e10adc3949ba59abbe56e057f20f883e' in the database."
            },
            "vpn": {
                "base": "A VPN (Virtual Private Network) establishes a secure, encrypted network connection over a public network.",
                "how_it_works": "It routes your internet traffic through an encrypted tunnel to a remote VPN server, hiding your IP address and encrypting data.",
                "why_important": "It protects internet traffic from interception on public Wi-Fi networks and secures remote work connections.",
                "applications": "Used by remote workers, privacy-focused users, and to bypass regional network restrictions.",
                "limitations": "VPNs do not make you anonymous to web tracking, and poor VPN providers can log and sell your browsing data.",
                "example": "For instance, using a VPN to safely access corporate servers while working from a local coffee shop's public Wi-Fi."
            },
            "intrusion detection system": {
                "base": "An Intrusion Detection System (IDS) is a system that monitors network traffic or system events for suspicious activity.",
                "how_it_works": "It compares traffic patterns to a database of known threats (Signature-based) or flags deviations from baseline activity (Anomaly-based).",
                "why_important": "It alerts administrators to active security breaches or policy violations in real-time.",
                "applications": "Deployed at critical network junctions (NIDS) and on critical servers (HIDS) to monitor integrity.",
                "limitations": "Can generate high volumes of false positives, which can overwhelm security analysts.",
                "example": "For instance, an IDS generating an alert when it detects multiple failed login attempts in a short period."
            }
        }
    }
}

QUESTION_PATTERNS = [
    "what is {}",
    "define {}",
    "explain {}",
    "can you explain {}",
    "give me an overview of {}",
    "what does {} mean",
    "describe {}",
    "tell me about {}",
    "how does {} work",
    "why is {} important",
    "what is the purpose of {}",
    "what are the applications of {}",
    "what are the benefits of {}",
    "what are the limitations of {}",
    "when is {} used",
    "where is {} used",
    "what are the main features of {}",
    "what is the role of {} in computer science",
    "explain {} for beginners",
    "explain {} in simple terms"
]

PREFIXES = [
    "",
    "please ",
    "briefly ",
    "clearly ",
    "in simple words, ",
    "for beginners, ",
    "technically, ",
    "academically, "
]

SUFFIXES = [
    "",
    "?",
    " in computer science",
    " in ai",
    " with example",
    " briefly",
    " in detail",
    " for interview",
    " for exam",
    " with simple explanation"
]

DIFFICULTY_RULES = {
    "easy": ["what is", "define", "describe", "tell me about", "what does"],
    "medium": ["how does", "why is", "what are the applications", "what are the benefits", "when is", "where is"],
    "hard": ["what are the limitations", "what is the role", "in detail", "technically", "academically"]
}

TOPIC_TAGS = {
    "networking": ["network", "protocols", "internet", "communication"],
    "machine_learning": ["ml", "models", "training", "prediction"],
    "deep_learning": ["neural-networks", "transformers", "representation-learning"],
    "nlp": ["language", "text", "tokens", "llm"],
    "databases": ["storage", "query", "retrieval", "data-management"],
    "operating_systems": ["os", "memory", "kernel", "processes"],
    "software_engineering": ["development", "api", "testing", "architecture"],
    "cybersecurity": ["security", "privacy", "protection", "risk"]
}


def infer_difficulty(question: str) -> str:
    q = question.lower()
    for level, patterns in DIFFICULTY_RULES.items():
        for p in patterns:
            if p in q:
                return level
    return "medium"


def generate_dynamic_answer(question: str, concept_data: dict, concept_name: str) -> str:
    q = question.lower()
    
    base = concept_data.get("base", "")
    how = concept_data.get("how_it_works", "")
    why = concept_data.get("why_important", "")
    apps = concept_data.get("applications", "")
    limits = concept_data.get("limitations", "")
    example = concept_data.get("example", "")
    
    parts = []
    
    if "how does" in q or "work" in q:
        parts.append(how)
    elif "why" in q or "important" in q or "purpose" in q or "role" in q:
        parts.append(why)
    elif "application" in q or "use" in q or "where" in q or "when" in q:
        parts.append(apps)
    elif "limitation" in q or "drawback" in q or "disadvantage" in q:
        parts.append(limits)
    else:
        parts.append(base)

    if "in simple words" in q or "simple terms" in q or "for beginners" in q:
        parts.insert(0, f"Simply put, {concept_name.upper()} is used to make this concept easy to understand.")
    elif "technically" in q or "academically" in q or "in detail" in q or "hard" in q:
        parts.append("From a technical perspective, it involves protocol/system-level specifications and constraints.")
        
    if "with example" in q or "example" in q:
        parts.append(example)
    elif "briefly" in q or "briefly" in q:
        return base
        
    full_answer = " ".join([p for p in parts if p])
    return full_answer


def build_entry(question, concept_data, topic, concept):
    dynamic_ans = generate_dynamic_answer(question, concept_data, concept)
    return {
        "question": question.strip(),
        "answer": dynamic_ans.strip(),
        "topic": topic,
        "concept": concept,
        "difficulty": infer_difficulty(question),
        "tags": TOPIC_TAGS.get(topic, []) + [concept.replace(" ", "-")],
        "source": "offline_mock"
    }


def generate_dataset():
    dataset = []
    seen = set()

    for topic_name, topic_data in TOPICS.items():
        for concept, concept_data in topic_data["concepts"].items():
            for pattern in QUESTION_PATTERNS:
                base_question = pattern.format(concept)

                for prefix in PREFIXES:
                    for suffix in SUFFIXES:
                        q = f"{prefix}{base_question}{suffix}".strip().lower()
                        q = " ".join(q.split())

                        if q not in seen:
                            seen.add(q)
                            dataset.append(build_entry(q, concept_data, topic_name, concept))

    return dataset


def expand_dataset(dataset, target_size=3000):
    expansions = [
        "step by step",
        "for students",
        "for researchers",
        "for developers",
        "for beginners",
        "in practical systems",
        "in real world applications",
        "in academic context",
        "in technical interviews",
        "from scratch"
    ]

    seen = {item["question"] for item in dataset}
    expanded = dataset[:]

    idx = 0
    while len(expanded) < target_size:
        item = dataset[idx % len(dataset)]
        
        topic_name = item["topic"]
        concept = item["concept"]
        concept_data = TOPICS[topic_name]["concepts"][concept]
        
        for phrase in expansions:
            new_q = f"{item['question']} {phrase}".strip().lower()
            new_q = " ".join(new_q.split())

            if new_q not in seen:
                seen.add(new_q)
                expanded.append(
                    build_entry(
                        new_q,
                        concept_data,
                        topic_name,
                        concept
                    )
                )

            if len(expanded) >= target_size:
                break
        idx += 1

    return expanded


def main():
    dataset = generate_dataset()
    dataset = expand_dataset(dataset, target_size=3200)

    with open("offline_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ Dynamic offline_data.json generated with {len(dataset)} records.")


if __name__ == "__main__":
    main()
