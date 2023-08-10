import pickle
import sys


class SafeUnpickler(pickle.Unpickler):

    # Dummy class to replace any whitelisted class during unpickling
    class DummyClass:
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return None

        def __setstate__(self, state):
            if not isinstance(state, dict):
                print("State is not a dictionary")

    def find_class(self, module, name):
        print(f"Unpickling is not allowed for {module}.{name}")
        return SafeUnpickler.DummyClass



def inspect_pkl(filename):
    # Display raw content
    # with open(filename, 'rb') as file:
    #     content = file.read()
    #     print("Raw content:")
    #     print(content)

    # Try to safely unpickle
    with open(filename, 'rb') as file:
        try:
            data = SafeUnpickler(file).load()
            print("\nDeserialized data:")
            print(data)
        except pickle.UnpicklingError as e:
            print(f"\nUnsafe pickle detected: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect.py <path_to_pkl_file>")
    else:
        inspect_pkl(sys.argv[1])
