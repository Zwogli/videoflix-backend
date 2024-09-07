# Videoflix-backend

In this section of my project I create my backend for a Netflix clone with a working registration, validation and verification. It should also be possible to watch global videos and upload your own videos to your account.
Python is used for my backend.

## 1. Creating the project

In the first part, I created the project and thought about the fact that my backend has several tasks to manage, which I divided into individual apps.
For version control, I decided to use GitHub and also created an online repository for my project.

## 2. the decision: First app authentication

There are many approaches that can and should be pursued. And yes, you should concentrate on your main feature first. However, many projects have a history and you have to make the best decision for yourself.

As I had a clear vision of registration, login and validation in my frontend, this already existed. Now I was at a crossroads.

Do I take care of the logic to create and validate a user or do I deal with my main feature where I still lack a bit of confidence and overview?

At this point, I decided in favour of creating the user. Why are you probably wondering? This has to do with my previous knowledge and personal judgement.

Through my previous projects I had to deal with login processes over and over again. Although they were always slightly different, the basic concept and what to look out for felt familiar. Of course, in my current project I also had to do a lot of looking up, googling and working with ChatGpt, but I hoped to see tangible results more quickly.

And I was right. I also used the time to realise my idea of my main feature.

## 3. Main Feature

After building my authentication, now I start with my main-feature. In the first step it was helpfull to realice what i should to do.

-   Creating video model. The focus was on creating a model in which you can save files.
-   Convert video files to diffrent sizes.
-   Upstream should work in the backgrouund.
-   Deleting file, all diffrent files from the same video must deleted
-   Change video size by streaming, if the datastrem bad
-   Automatic creation of a thumpnail when uploading

## 4. Deployment