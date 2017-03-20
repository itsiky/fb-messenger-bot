# fb-messenger-bot

A FB Messenger bot Python app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Create a Facebook page

Documentation can be found here [facebook for developers](https://developers.facebook.com/docs/messenger-platform)

If you don’t already have one, you need to [create a Facebook Page](https://www.facebook.com/pages/create/). The Facebook Page is the “identity” of your bot, including the name and image that appears when someone chats with it inside Facebook Messenger.

If you’re just creating a dummy one for your chatbot, it doesn’t really matter what you name it or how you categorize it. You can skip through most of the setup steps.

In order to communicate with your bot, people will need to go through your Page, which we’ll look at in a bit.

## Create a Facebook App
Go to the [Facebook Developer’s Quickstart](https://developers.facebook.com/quickstarts/?platform=web) Page and click “Skip and Create App ID” at the top right. Then create a new Facebook App for your bot and give your app a name, category and contact email.

You’ll see your new App ID at the top right on the next page. Scroll down and click “Get Started” next to Messenger.

## Setup Your Messaging App

Now you’re in the Messenger settings for your Facebook App. There are a few things in here you’ll need to fill out in order to get your chatbot wired up to the Heroku endpoint we setup earlier.

- Generate a Page Access Token
Using the Page you created earlier (or an existing Page), click through the auth flow and you’ll receive a Page Access Token for your app.

Click on the Page Access Token to copy it to your clipboard. You’ll need to set it as an environment variable for your Heroku application

## Setup a webhook

When you go to setup your webhook, you’ll need a few bits of information:

Callback URL - The Heroku (or other) URL that we setup earlier.
Verification Token - A secret value that will be sent to your bot, in order to verify the request is coming from Facebook. Whatever value you set here, make sure you add it to your Heroku environment using heroku config:add

VERIFY_TOKEN=your_verification_token_here

Subscription Fields - This tells Facebook what messaging events you care about and want it to notify your webhook about. If you're not sure, just start with "messages," as you can change this later

After you’ve configured your webhook, you’ll need to subscribe to the specific page you want to receive message notifications for.

Once you’ve gotten your Page Access Token and set up your webhook, make sure you set both the PAGE_ACCESS_TOKEN and VERIFY_TOKEN config values in your Heroku application, and you should be good to go!

## Config Wit.ai bot

Wit.ai documentation on how to build your first conversational app
[Go to Docs](https://wit.ai/docs/quickstart)


## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku config:add VERIFY_TOKEN=your_verification_token_here
$ heroku config:add PAGE_ACCESS_TOKEN=your_copied_token_goes_here_too

$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
- [Wit.ai](https://wit.ai/docs)
