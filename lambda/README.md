lambda function management
==========================

This is my first attempt at building some sort of workflow around deploying
and managing AWS functions. This is a collection scripts and tools to help
manage slater's backend Lambda functions. See descriptions and usage examples
below.

#### updateLambda

This bash script is responsible for updating the code of an existing Lambda
function. The first argument is the name of the Lambda function *and* the
name of the subdirectory in which the code lies. The second is the region
where the existing Lambda function resides. Here is an example usage:

```
./updateLambda.sh slaterLogin us-east-1
```

If you want to add psycopg2 to the package, updateLambda includes a special
by which you can install the psycopg package into your zip file. Do so by
making a call such as this:

```
./updateLambda.sh -p slaterLogin us-east-1
```
