from .engine import Engine

if __name__ == "__main__":
    import numpy as np
    import scared

    ths = scared.traces.read_ths_from_ets_file("../../examples/traces/stagegate1.ets")

    selection_function = scared.aes.selection_functions.encrypt.FirstSubBytes()

    att = scared.CPAAttack(
        selection_function=selection_function,
        model=scared.HammingWeight(),
        discriminant=scared.maxabs,
    )

    container = scared.Container(ths, frame=range(0, 3000))
    att.run(container)

    recovered_masterkey = np.argmax(att.scores, axis=0).astype("uint8")
    print(recovered_masterkey)

    recomputed_ciphertexts = scared.aes.encrypt(ths.plaintext, recovered_masterkey)
    print(np.array_equal(recomputed_ciphertexts, ths.ciphertext))
