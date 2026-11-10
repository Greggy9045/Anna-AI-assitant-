import json 

'''
You are about to view what a week of late night coding sessions 
look like, i started this everyday at 2 am and finish it at 6 am 
for week ! I know if its a fucking mess but it works YAY !
'''

def vocab_filler(filename):
    with open(filename, 'r') as file:
        return file.read()

class Tokenizer:
    def __init__(self):
        self.largest_ID = 0
        self.count_pairs_ID = 0

        self.vocab = {}
        self.errors = {}
        self.temp_msg = []
        self.char_list = {}
        self.merge_pairs = {}
        self.merge_rules = []
        self.count_pairs = {}
        self.current_message = []

        self.no = False
        self.yes = True

    def save_vocab(self, file="vocab.json"):
            try:
                self._update_largest_ID()
    
                with open(file, "w", encoding="utf-8") as f:
                    json.dump({
                        "char_list": self.char_list, 
                        "merge_pairs": self.merge_pairs,
                        "merge_rules": self.merge_rules
                        }, f, ensure_ascii=self.no, indent=4)
            except FileNotFoundError as e:
                self.errors[e] = "file wasnt found"

    def load_vocab(self, file="vocab.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    self.char_list = data["char_list"]
                    self.merge_pairs = data["merge_pairs"]
                    self.merge_rules = [(tuple(pair), token_ID) for pair, token_ID in data["merge_rules"]]
                    self._update_largest_ID()

            except json.decoder.JSONDecodeError as e:
                self.errors[e] = "vocab.json file is/was empty"
            except FileNotFoundError as e:
                self.errors[e] = "file wasnt found"

    def _update_largest_ID(self):
        token_IDs = list(self.char_list.values()) + list(self.merge_pairs.values())
        token_IDs.extend(token_ID for _, token_ID in self.merge_rules)
        self.largest_ID = max(token_IDs, default=0)

    def count_adajcent_pairs(self):
        self.count_pairs.clear()

        for first, second in zip(self.current_message, self.current_message[1:]):
            self.count_pairs[(first, second)] = self.count_pairs.get((first, second), 0) + 1
            
        return self.count_pairs

    def most_common_pair(self):
        return max(self.count_pairs, key=self.count_pairs.get)

    def merge_pair(self, max_pair, training): 
        merged_pair = ""
        index = 0
        new_msg = []

        for i in max_pair :
            merged_pair += next((k for k, v in {**self.char_list, **self.merge_pairs}.items() if v == i), "")

        if training == self.yes : # we are live bitches !!!!!!!!!!!!!!!!!!!!!!!!!!!
            token_ID = next((token_ID for pair, token_ID in self.merge_rules if tuple(pair) == max_pair), None)
            if token_ID is None:
                self.largest_ID += 1
                token_ID = self.largest_ID
                self.merge_rules.append((max_pair, token_ID))

            self.merge_pairs[merged_pair] = token_ID
        else:
            token_ID = self.merge_pairs[merged_pair]

        while index < len(self.current_message):
            if tuple((self.current_message[index:index + 2])) == max_pair:
                index += 2
                new_msg.append(token_ID)
            else:
                new_msg.append(self.current_message[index])
                index += 1

        self.current_message = new_msg

        return self.current_message

    def encode(self, msg):
        self.current_message.clear()

        for char in msg:
            if char not in self.char_list:
                raise ValueError(f"Unknown character: {char}")

            self.current_message.append(self.char_list[char])

        for pair, token_ID in self.merge_rules:
            index = 0
            new_msg = []

            while index < len(self.current_message):
                curr_pair = tuple(self.current_message[index:index + 2])

                if curr_pair == pair:
                    new_msg.append(token_ID)
                    index += 2
                else:
                    new_msg.append(self.current_message[index])
                    index += 1

            self.current_message = new_msg

        return self.current_message

    def decode(self, token_ID):
        found_ID = []

        for i in token_ID :
            for item, value in self.char_list.items():
                if i == value:
                    found_ID.append(item)

            for item, value in self.merge_pairs.items():
                if i == value:
                    found_ID.append(item)
        return "".join(found_ID)

    def tokenize(self, msg):
        self.current_message.clear()

        for word in msg:
            if word not in self.char_list:
                self.largest_ID += 1
                self.char_list[word] = self.largest_ID

            self.current_message.append(self.char_list[word])

        self.count_adajcent_pairs()

        return self.current_message

    def train(self, msg, amount):
        self.tokenize(msg)

        for i in range(amount):
            self.count_adajcent_pairs()

            if not self.count_pairs:
                break

            self.merge_pair(self.most_common_pair(), training=self.yes)
    
tokenizer = Tokenizer()

def test_tokenizer(tokenizer):
    test_cases = [
        "",                          # Empty string
        "a",                         # Single character
        "aaaaaaaa",                  # Repeated characters
        "hello world",               # Spaces
        "hello!!!",                  # Punctuation
        "hello\nworld",              # Newline
        "café",                      # Unicode
        "1234567890",                # Numbers
        "The dead cat is beautiful! :)"  # Mixed input
    ]

    passed = 0
    failed = 0

    print("\n========== TOKENIZER TESTS ==========\n")

    for original in test_cases:
        try:
            encoded = tokenizer.encode(original)
            decoded = tokenizer.decode(encoded)

            if decoded == original:
                print(f"[PASS] {repr(original)}")
                passed += 1
            else:
                print(f"[FAIL] {repr(original)}")
                print(f"       Expected: {repr(original)}")
                print(f"       Got:      {repr(decoded)}")
                failed += 1

        except Exception as error:
            print(f"[ERROR] {repr(original)}")
            print(f"        {type(error).__name__}: {error}")
            failed += 1

    print("\n========== RESULTS ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    return failed == 0

tokenizer.load_vocab()

#tokenizer.train(vocab_filler("test.txt"), 10)

test_tokenizer(tokenizer=tokenizer)

tokenizer.save_vocab()
