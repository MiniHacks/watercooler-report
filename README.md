
# Watercooler Report

*Detects and relays incidences of workplace harassment on Slack and over email.*

## Prizes

Best Overall  
Best Use of Cloud Resources  
Best Use of Google Cloud 

## Inspiration

Victims of harassment often fear that there will be backlash if they report incidents. Programmatically detecting them takes the burden off the victims of harassment while still preserving privacy.

**Watercooler Report** will *automatically* identify and report cases of sexual harassment going on over Slack or email then relay them to an authority figure. **No longer will three out of every four sexual harassment cases go unreported.**

One the most impressive features is that the model has a sophisticated attention mechanism and is an LSTM so we are not purely dependent on keywords. The model can understand metaphors and is great at flagging so-called "benevolent" sexism such as humor that reinforces gender stereotypes. The judgements are also not specifically tied to gender identity, the bot can also detect harassment against men and those with other identities.

## How we built it

- **FastAPI REST API** microservice to host the ML model. The model is a **biLSTM** with an attention mechanism based on **GloVe** embeddings. We tried alternatives, including **gradient-boosted trees** (didn't provide as effective of a gradient), **logistic regression** from embeddings (worse accuracy) and several permutations of **LSTMs**. The model is hosted on **Google Compute Engine** and most of the development was done there due to dependency issues.
- **Slack** bot with **Twilio** as an alternative notification mechanism, built with **Flask**, hosted on a **Google Compute Engine** instance and forwarded via **nginx**.
- **Google Workspaces** integration to survey emails from an organization and forward them to an administrator if the model flags them.
- **Domain.com** to get a domain for our mailserver (and API, not that anyone will see that).
- We wrote code to use **Google Cloud Storage** and **Google Cloud Speech** to upload and then transcribe blobs of audio or video, though we did not end up using it in our integrations.

## Challenges we ran into

- We had to be very conscientious about our choice of issue to find an area where we could meaningfully empower women despite our lack of insight (as four guys)
- We originally planned to have a web app that would process media but realized that put too much of a burden on the user. Late on Saturday afternoon we decided to pivot to Slack and Gmail where there is ample information to process.
- Python dependencies were a major hassle. Our primarily ML engineer has an M1 Mac, which despite being advertised as great for machine learning is very resistant to running Tensorflow and such.

## Accomplishments that we're proud of

- Integrations on multiple major platforms.
- Rolling our own machine learning models and assessing which one of them is most effective.
- Deploying more than 8 minutes before the deadline (closer to 8 hours!).

## What's Next?

- Publicly available Slack integration and Google Work-space add-on
- Explore intervention measures for the bot, especially in the case of "benevolent" sexism that perpetuates norms.
- Provide alternative ways of interacting with reports rather than just emails or slack DMs. Perhaps a dashboard.

## Resources

Grosz, Dylan, and Patricia Conde-Cespedes. “Automatic Detection of Sexist Statements Commonly Used at the Workplace.” ArXiv:2007.04181 [Cs], July 8, 2020. http://arxiv.org/abs/2007.04181.

- Paper outlining several architectures to detect both "hostile" (overt) and "benevolent" (latent or systematic) harassment as described by the ambivalent sexism model.

Grosz, Dylan. "Sexist Workplace Statements." April 27, 2020. https://www.kaggle.com/dgrosz/sexist-workplace-statements

- Curated dataset featuring statements from a variety of sourced, curated to avoid biases in previous data sets. (For example, many models consider the name "Kat" to be sexist since many comments were directed at her during season 6 of My Kitchen Rules)

"Gao-20-564, Workplace Sexual Harassment." September 1, 2020. https://www.gao.gov/assets/gao-20-564.pdf.

- Used for statistics on workplace harassment.

