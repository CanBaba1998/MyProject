import random

from .model import GuessAWord

games = {

}


class GuessAWordGame:

    current_game = None

    def fetch_game(self):
        """
        Geben Sie einfach das aktuelle_spiel zurück
        """
        return self.current_game

    def get_game(self, channel_id):
        """
        Lädt das Spiel in current_game
        """
        self.current_game = None
        for g in games.keys():
            if channel_id == g:
                self.current_game = games[g]

    def new_round(self, channel):
        """
        löscht das aktuelle Spiel und überschreibt das Kanalspiel mit einem neuen und beginnt eine neue Runde        
        """
        self.current_game = None
        new_game = self.create_game_instance(channel.id, channel.name)
        self.save(new_game)
        self.get_game(channel.id)

    def guess(self, channel_id, guess):
        """
        Lassen Sie den Benutzer das Wort erraten   
        """
        self.get_game(channel_id)
        if self.current_game is None:
            return None
        # start playing the game
        return self.current_game.guess(guess)

    def create_game_instance(self, channel_id, channel_name):
        """
        Erstellt ein neues Gaw-Spiel
        """
        random_instance = self.get_random_word()
        new_game = GuessAWord(
            random_instance['word'], random_instance['category'])
        new_game.channel_id = channel_id
        new_game.channel_name = channel_name
        return new_game

    async def start_game(self, guild, author, players):
        """
        Startet ein neues Spiel in einem neuen Kanal, lädt Leute ein, setzt Berechtigungen etc.
        """
        channel_name = "gaw-game-%s" % author.name
        existing_channel = self.get_channel_by_name(guild, channel_name)
        if existing_channel is None:
            channel = await self.create_channel(guild, channel_name)
            await self.set_permissions(guild, channel, players)

            new_game = self.create_game_instance(channel.id, channel.name)

            self.save(new_game)
            self.get_game(channel.id)

            return channel

        return None

    def save(self, game):
        """
        Speichert ein Spiel nach Kanal-ID im Games-Objekt
        """
        games[game.channel_id] = game

    async def destroy(self, guild, channel_id):
        """
        Entfernt das Spiel aus dem Spielobjekt und löscht den Kanal
        """
        games.pop(channel_id)
        await self.delete_channel(guild, channel_id)

    async def delete_channel(self, guild, channel_id):
        """
        Löscht einen Textkanal anhand seiner ID
        """
        channel = guild.get_channel(channel_id)
        await channel.delete()

    async def set_permissions(self, guild, channel, players):
        """
        Legt die Berechtigung für einen Kanal für die default_role des Servers fest
        und discord.Member-Objekte
        """
        await channel.set_permissions(guild.default_role, view_channel=False, send_messages=False)

        for p in players:
            await channel.set_permissions(p, view_channel=True, send_messages=True)

    async def create_channel(self, guild, channel_name):
        """
        Erstellt einen neuen Kanal in der Kategorie "Spiel"
        """
        category = self.get_category_by_name(guild, "Games")
        await guild.create_text_channel(channel_name, category=category)
        channel = self.get_channel_by_name(guild, channel_name)
        return channel

    def get_channel_by_name(self, guild, channel_name):
        """
        Channel-Objekt nach channel_name abrufen
        """
        channel = None
        for c in guild.channels:
            if c.name == channel_name.lower():
                channel = c
                break
        return channel

    def get_category_by_name(self, guild, category_name):
        """
        Kategorieobjekt nach Kategoriename abrufen
        """
        category = None
        for c in guild.categories:
            if c.name == category_name:
                category = c
                break
        return category

    def get_random_word(self):
        """
        Holen Sie sich ein zufälliges Wort für unser Gaw-Spiel
        """
        return random.choice([
            {
                'word': "python",
                'category': "Development"
            },
            {
                'word': "tree",
                'category': "Nature"
            },
            {
                'word': "audi",
                'category': "Cars"
            },
            {
                'word': "Discord",
                'category': "Companies"
            },
        ])
