# Boldify
Boldify is a steganographic encryption scheme that hides a message within another message using bold letters. This site is the official encoding and decoding engine of this scheme. Note no messages are stored and hence complete privacy is maintained. You can test it online here(https://boldify.vercel.app/).

# Encryption
Boldify uses a Markov Chain Generator to generate random sentences based on sample text, which is provided in the data.txt file(it is currently defaulted to a chapter of The Hitchhiker's Guide to the Galaxy). As a result, in order to encrypt a message, you will just need to enter the message and submit the form. Note if the message is too long, it may return an error. This may be addressed in a future release. Also, note that this encryption is not deterministic as the Markov Chain Generator is not deterministic, as a result, the same message may be encrypted in many different ways and may even result in errors.

# Decryption
Boldify provides a rich text box from the CKEditor to enter encrypted messages as encryptions are in bolded form. This then reads out only the bolded letters and gives the corresponding plaintext of the message. Note that this can be used to decrypt manual encryptions faster and does not require the use of the Boldify encrypter though it is faster.
