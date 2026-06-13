import json
import random

random.seed(42)

TOPICS = {
    "networking": {
        "concepts": {
            "tcp": "TCP (Transmission Control Protocol) is a connection-oriented transport protocol that provides reliable, ordered, and error-checked delivery of data between applications. It is widely used in web communication, file transfer, and email systems.",
            "udp": "UDP (User Datagram Protocol) is a connectionless transport protocol that sends packets without establishing a session. It is faster than TCP but does not guarantee delivery, order, or retransmission, making it suitable for streaming, gaming, and VoIP.",
            "ip": "IP (Internet Protocol) is the core protocol used for addressing and routing packets across networks. It allows devices to communicate by assigning unique addresses and forwarding packets toward their destinations.",
            "dns": "DNS (Domain Name System) is a naming system that translates human-readable domain names into IP addresses so computers can locate services on the internet.",
            "http": "HTTP (Hypertext Transfer Protocol) is an application-layer protocol used for transferring web pages and related resources between clients and servers.",
            "https": "HTTPS is the secure version of HTTP that uses TLS/SSL encryption to protect data transferred between clients and servers.",
            "router": "A router is a networking device that forwards packets between different networks and determines the best path for data transmission.",
            "switch": "A switch is a network device that connects devices within the same local area network and forwards frames based on MAC addresses.",
            "firewall": "A firewall is a network security mechanism that monitors and controls incoming and outgoing traffic based on predefined security rules.",
            "nat": "NAT (Network Address Translation) is a technique that maps private IP addresses to public IP addresses, helping conserve address space and improve security."
        }
    },
    "machine_learning": {
        "concepts": {
            "machine learning": "Machine learning is a branch of artificial intelligence that enables systems to learn patterns from data and improve performance without being explicitly programmed for every case.",
            "supervised learning": "Supervised learning is a machine learning approach where models are trained using labeled examples consisting of inputs and correct outputs.",
            "unsupervised learning": "Unsupervised learning is a machine learning approach that finds patterns, clusters, or structures in data without labeled outputs.",
            "reinforcement learning": "Reinforcement learning is a machine learning paradigm in which an agent learns by interacting with an environment and receiving rewards or penalties.",
            "overfitting": "Overfitting happens when a model learns the training data too closely, including noise, and performs poorly on unseen data.",
            "underfitting": "Underfitting occurs when a model is too simple to learn the important patterns in the data, resulting in poor performance.",
            "feature engineering": "Feature engineering is the process of selecting, transforming, or creating input features to improve model performance.",
            "training dataset": "A training dataset is the portion of data used to teach a machine learning model by adjusting its internal parameters.",
            "validation set": "A validation set is a subset of data used during model development to tune hyperparameters and monitor generalization.",
            "test set": "A test set is a separate dataset used to evaluate the final performance of a trained model on unseen data."
        }
    },
    "deep_learning": {
        "concepts": {
            "deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn complex representations from large amounts of data.",
            "neural network": "A neural network is a computational model made of interconnected neurons organized in layers, designed to learn mappings from inputs to outputs.",
            "cnn": "A CNN (Convolutional Neural Network) is a deep learning architecture specialized for grid-like data such as images, using convolutional filters to detect patterns.",
            "rnn": "An RNN (Recurrent Neural Network) is a neural network architecture designed for sequential data, where previous information influences future computation.",
            "lstm": "LSTM (Long Short-Term Memory) is a type of recurrent neural network designed to better capture long-range dependencies in sequences.",
            "attention": "Attention is a mechanism that allows a model to focus on the most relevant parts of the input when processing information.",
            "transformer": "The Transformer is a deep learning architecture based on self-attention, widely used in modern NLP and large language models.",
            "self-attention": "Self-attention is a mechanism that measures the importance of each token relative to other tokens in the same sequence.",
            "embedding": "An embedding is a dense vector representation of data that captures semantic or structural meaning in numerical form.",
            "fine-tuning": "Fine-tuning is the process of adapting a pretrained model to a specific task or domain by training it further on a relevant dataset."
        }
    },
    "nlp": {
        "concepts": {
            "natural language processing": "Natural Language Processing (NLP) is a field of AI focused on enabling computers to understand, analyze, and generate human language.",
            "tokenization": "Tokenization is the process of breaking text into smaller units such as words, subwords, or characters for language processing.",
            "stemming": "Stemming is a text normalization technique that reduces words to their root or base form by removing suffixes.",
            "lemmatization": "Lemmatization reduces words to their dictionary base form while considering their linguistic meaning and context.",
            "named entity recognition": "Named Entity Recognition (NER) is the task of identifying entities such as people, organizations, and locations in text.",
            "sentiment analysis": "Sentiment analysis is the task of determining the emotional tone or opinion expressed in a piece of text.",
            "language model": "A language model estimates the probability of sequences of words or tokens and is used in tasks such as prediction and text generation.",
            "bert": "BERT is a transformer-based language model that reads text bidirectionally to better understand contextual meaning.",
            "gpt": "GPT is a family of generative transformer-based language models trained to predict the next token and generate coherent text.",
            "prompt engineering": "Prompt engineering is the practice of designing effective prompts to guide the behavior of large language models."
        }
    },
    "databases": {
        "concepts": {
            "database": "A database is an organized collection of data that can be efficiently stored, queried, updated, and managed.",
            "sql": "SQL (Structured Query Language) is a language used to manage and query relational databases.",
            "nosql": "NoSQL refers to database systems designed for flexible schemas, scalability, and high-performance storage of non-tabular data.",
            "indexing": "Indexing is a technique used in databases to speed up data retrieval by creating efficient lookup structures.",
            "normalization": "Normalization is the process of organizing relational database tables to reduce redundancy and improve consistency.",
            "acid": "ACID stands for Atomicity, Consistency, Isolation, and Durability, which are core properties of reliable database transactions.",
            "transaction": "A transaction is a sequence of database operations treated as a single unit of work.",
            "primary key": "A primary key is a unique identifier for each record in a database table.",
            "foreign key": "A foreign key is a field in one table that references the primary key of another table, establishing a relationship.",
            "vector database": "A vector database is a database optimized for storing and searching embeddings using similarity search."
        }
    },
    "operating_systems": {
        "concepts": {
            "operating system": "An operating system is system software that manages hardware resources and provides services for computer programs.",
            "process": "A process is an instance of a program in execution, including its memory, state, and system resources.",
            "thread": "A thread is the smallest unit of execution within a process and allows concurrent operations.",
            "scheduling": "Scheduling is the operating system mechanism that determines which process or thread gets CPU time.",
            "deadlock": "Deadlock is a state where two or more processes are unable to proceed because each is waiting for resources held by another.",
            "virtual memory": "Virtual memory is a memory management technique that gives processes the illusion of large contiguous memory using disk and RAM.",
            "paging": "Paging is a memory management technique that divides memory into fixed-size blocks called pages.",
            "kernel": "The kernel is the core component of an operating system that manages hardware, memory, and system calls.",
            "system call": "A system call is an interface through which user programs request services from the operating system kernel.",
            "file system": "A file system is the method an operating system uses to store, organize, and retrieve files on storage devices."
        }
    },
    "software_engineering": {
        "concepts": {
            "software engineering": "Software engineering is the disciplined application of engineering principles to the design, development, testing, and maintenance of software systems.",
            "api": "An API (Application Programming Interface) defines rules and methods that allow software components to communicate with each other.",
            "rest api": "A REST API is an architectural style for web services that uses HTTP methods and resource-based URLs.",
            "microservices": "Microservices is a software architecture approach where applications are built as small, independent services.",
            "version control": "Version control is a system for tracking changes in source code and coordinating collaborative software development.",
            "git": "Git is a distributed version control system used to manage source code history and collaboration.",
            "testing": "Software testing is the process of evaluating software to verify that it meets requirements and behaves as expected.",
            "unit testing": "Unit testing is the practice of testing small, isolated parts of a software application such as functions or methods.",
            "debugging": "Debugging is the process of finding, analyzing, and fixing defects or unexpected behavior in software.",
            "refactoring": "Refactoring is the process of improving the internal structure of code without changing its external behavior."
        }
    },
    "cybersecurity": {
        "concepts": {
            "cybersecurity": "Cybersecurity is the practice of protecting systems, networks, and data from unauthorized access, attacks, and damage.",
            "encryption": "Encryption is the process of converting readable data into an unreadable format to protect confidentiality.",
            "phishing": "Phishing is a social engineering attack in which attackers trick users into revealing sensitive information.",
            "malware": "Malware is malicious software designed to disrupt, damage, or gain unauthorized access to systems.",
            "ransomware": "Ransomware is a type of malware that encrypts a victim's data and demands payment for restoration.",
            "authentication": "Authentication is the process of verifying the identity of a user, device, or system.",
            "authorization": "Authorization is the process of determining what actions or resources an authenticated user is allowed to access.",
            "hashing": "Hashing is the process of converting input data into a fixed-length value, often used for integrity checks and password storage.",
            "vpn": "A VPN (Virtual Private Network) creates a secure encrypted tunnel for communication over public networks.",
            "intrusion detection system": "An intrusion detection system monitors network or system activity to detect suspicious behavior or attacks."
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


def build_entry(question, answer, topic, concept):
    return {
        "question": question.strip(),
        "answer": answer.strip(),
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
        for concept, answer in topic_data["concepts"].items():
            for pattern in QUESTION_PATTERNS:
                base_question = pattern.format(concept)

                for prefix in PREFIXES:
                    for suffix in SUFFIXES:
                        q = f"{prefix}{base_question}{suffix}".strip().lower()
                        q = " ".join(q.split())

                        if q not in seen:
                            seen.add(q)
                            dataset.append(build_entry(q, answer, topic_name, concept))

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
        for phrase in expansions:
            new_q = f"{item['question']} {phrase}".strip().lower()
            new_q = " ".join(new_q.split())

            if new_q not in seen:
                seen.add(new_q)
                expanded.append(
                    build_entry(
                        new_q,
                        item["answer"],
                        item["topic"],
                        item["concept"]
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

    print(f"✅ offline_data.json generated with {len(dataset)} records.")


if __name__ == "__main__":
    main()
