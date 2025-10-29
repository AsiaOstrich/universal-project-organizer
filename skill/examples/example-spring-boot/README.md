# Example Spring Boot Project

This is an example Spring Boot project with Universal Project Organizer configuration.

## Template

This project uses the **spring-boot** template from Universal Project Organizer. The template was initialized with:

```bash
python skill/scripts/init_project.py --template spring-boot
```

## Configuration

The project configuration is in `.claude/project.yaml`. This file was generated from the spring-boot template and can be customized for your specific needs.

## Defined File Types

- **service** - Business logic services
- **controller** - REST API controllers
- **repository** - Data access repositories
- **model** - Domain models/entities
- **config** - Configuration classes
- **dto** - Data Transfer Objects

## Usage

With this configuration, you can ask Claude to generate files:

```
"Create a UserService"
→ Generates: src/main/java/com/example/demo/service/UserService.java
→ Generates: src/test/java/com/example/demo/service/UserServiceTest.java

"Create a ProductController"
→ Generates: src/main/java/com/example/demo/controller/ProductController.java
→ Generates: src/test/java/com/example/demo/controller/ProductControllerTest.java
```

## Validation

Validate the configuration:

```bash
python skill/scripts/validate_config.py skill/examples/example-spring-boot
```