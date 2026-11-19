def CONDITION_VERIFIER(df):
    long_MA_deviation = 150
    sma34_LONG_ENTRY_variation = 200
    
    short_MA_deviation = 100
    sma34_SHORT_ENTRY_variation = 200
    
    last_5ema_value = float(df['ema_5'].iloc[-1])
    last_34ema_value = float(df['sma_34'].iloc[-1])
    fifth_34ema_value = float(df['sma_34'].iloc[-5])
    last_atr_value = float(df['atr'].iloc[-1])
    
    atr_rule = last_atr_value > 210
    
    # Long Trading conditions
    l1 = last_5ema_value > last_34ema_value
    l2 = (last_5ema_value - last_34ema_value) > long_MA_deviation
    l3 = (last_34ema_value - fifth_34ema_value) > sma34_LONG_ENTRY_variation
    
    # Short Trading conditions
    s1 = last_5ema_value < last_34ema_value
    s2 = (last_34ema_value - last_5ema_value) > short_MA_deviation
    s3 = (fifth_34ema_value - last_34ema_value) > sma34_SHORT_ENTRY_variation
    
    long_entry_condition = l1 and (l2 or l3) and atr_rule
    short_entry_condition = s1 and (s2 or s3) and atr_rule
    
    return long_entry_condition, short_entry_condition