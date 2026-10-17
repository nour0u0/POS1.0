import os
import importlib.util


MIGRATION_FOLDER = "DB/Migration"


def run_migrations():

    if not os.path.exists(MIGRATION_FOLDER):
        print("Migration folder not found")
        return


    files = sorted(
        os.listdir(MIGRATION_FOLDER)
    )


    for file in files:

        if not file.endswith(".py"):
            continue

        if file == "__init__.py":
            continue


        path = os.path.join(
            MIGRATION_FOLDER,
            file
        )


        print(f"Running migration: {file}")


        spec = importlib.util.spec_from_file_location(
            file[:-3],
            path
        )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(
            module
        )


        # If the migration contains migrate()
        if hasattr(module, "migrate"):
            module.migrate()

        else:
            print(
                f"{file} has no migrate() function"
            )


    print("All migrations completed")


if __name__ == "__main__":
    run_migrations()