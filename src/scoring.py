import pandas as pd

def get_priority_label(score):
    if score >= 0.70:
        return "HIGH"
    elif score >= 0.40:
        return "MEDIUM"
    else:
        return "LOW"

def score_rfqs(df):
    df = df.copy()

    # Basic features
    df["abs_underlying_move_pct"] = df["underlying_move_pct"].abs()
    df["abs_iv_change"] = df["iv_change"].abs()

    # Staleness risk
    df["age_score"] = (df["time_since_last_price_update_min"] / 15).clip(0, 1)

    df["recent_move_score"] = (df["underlying_move_5m_pct"].abs() / 2).clip(0, 1)

    df["recent_iv_score"] = (df["iv_change_5m"].abs() / 3).clip(0, 1)

    df["recent_market_score"] = (
        0.7 * df["recent_move_score"]+ 0.3 * df["recent_iv_score"])

    df["staleness_risk"] = (
        df["age_score"]* (0.3 + 0.7 * df["recent_market_score"])
    )


    # Priority components

    # 2M+ notional = maximum size score
    df["size_score"] = (df["notional"] / 2_000_000).clip(0, 1)

    # 0% from barrier = max risk, 30%+ = zero
    df["barrier_risk_score"] = (
        1 - df["distance_to_barrier_pct"] / 30).clip(0, 1).fillna(0)

    # 5%+ daily underlying move = maximum score
    df["market_move_score"] = (df["abs_underlying_move_pct"] / 5).clip(0, 1)

    # 8+ vol points change = maximum score
    df["iv_score"] = (df["abs_iv_change"] / 8).clip(0, 1)

    # Final priority score
    df["priority_score"] = (
        0.35 * df["barrier_risk_score"]
        + 0.20 * df["market_move_score"]
        + 0.15 * df["iv_score"]
        + 0.15 * df["staleness_risk"]
        + 0.15 * df["size_score"]
    )

    df["priority"] = df["priority_score"].apply(get_priority_label)
    
    return df