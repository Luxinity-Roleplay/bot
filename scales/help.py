from dis_snek import slash_command, slash_option, OptionTypes, Scale
from algoliasearch.search_client import SearchClient

import datetime
import dis_snek


class help(Scale):
    def __init__(self, ctx):
        ## Fill out from trying a search on the madeline docs
        app_id = "SP47F92EMX"
        api_key = "b686c04a3cb99263c386c1519bbdc9d7"
        self.search_client = SearchClient.create(app_id, api_key)
        self.index = self.search_client.init_index("docs")

    @slash_command("luxinity-wiki", description="Scour our wiki for an article")
    @slash_option(
        name="article_name",
        description="Name of the article to find",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def wiki(self, ctx, *, article_name):
        results = await self.index.search_async(article_name)
        description = ""
        hits = []
        for hit in results["hits"]:
            title = self.get_level_str(hit["hierarchy"])
            if title in hits:
                continue
            hits.append(title)
            url = hit["url"]
            description += f"[{title}]({url})\n"
            if len(hits) == 10:
                break
        embed = dis_snek.Embed(
            title="Your help has arrived!",
            description=description,
            color=0x7289DA,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)

    def get_level_str(self, levels):
        last = ""
        for level in levels.values():
            if level is not None:
                last = level
        return last


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    help(bot)
