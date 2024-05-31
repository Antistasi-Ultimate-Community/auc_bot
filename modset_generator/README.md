## modsets
Can be a list of modsets (in [json/modsets.json](https://github.com/Antistasi-Ultimate-Community/auc_bot/blob/main/json/modsets.json)). For example, `rhs,3cbf,3cbbaf` - Note the lack of spaces, this is intentional and will break without them.

If set to `all`, it will use every possible modset.

## climates
Can be multiple climates or a singular climate. For example `arid,temperate` will return any factions matching either climate. `arid` will just return factions matching arid.

If set to `all` it will use all 4 standard climates.

## era
Current eras are: `modern,scifi,lowtech,coldwar,stalker`

## key
Current keys are: `vanilla,rhs`

## dlc
If `none` is in the argument, it will include every faction that requires no dlc (RHS and CUP, for example).

If `ws` is in the argument, it will include every faction that requires Western Sahara (Aegis and WS factions for example).

Current dlcs are: `vanilla,ws,gm,vn,none`

## double_occ
Has to be true or false. If set to true, the invader and occupier pools are merged.

# Deprecated Choices 

### (Ignore these unless manually hosting the bot yourself)

## "choices"
The amount of choices you want. Has to be an int.
The above option is deprecated in the discord bot (this) version, and is hardcapped to 1 unless you're hosting the bot and change it manually in [json/settings.json](https://github.com/Antistasi-Ultimate-Community/auc_bot/blob/main/json/settings.json)

## "debug_level"
The amount of debug messages you'll get. You usually don't need to change this, but anything higher than 0 will give you debug information.

Deprecated like above. Check [json/settings.json](https://github.com/Antistasi-Ultimate-Community/auc_bot/blob/main/json/settings.json).

## "force_faction_x"
Has to be an array in format `["faction_type", "faction"]`. This ignores all the other "desired" settings.

For example, if you want to force RHS AFRF as occupant it would be: 

`"force_faction_occ": ["factionsInv", "RHS_AFRF"]`

If set to `[]` it will not force any faction. This is the same for all of the below respectively.

### "force_faction_occ"

### "force_faction_inv"

### "force_faction_reb"

### "force_faction_riv"

### "force_faction_civ"
