"""Format games DataFrame for gui graphs."""
import pandas as pd


def get_time_classes_and_checklist_options(df: pd.DataFrame) -> tuple:
    """Get time class checklist options.

    :param: pd.DataFrame df: Dataframe with time_class column.
    :return: Checklist options.
    :rtype: tuple.
    """
    time_classes = df['time_class'].unique()
    return [
        {"label": col.split("_")[0].title(), "value": col}
        for col in time_classes
    ], time_classes


def get_most_common_ecos(df: pd.DataFrame, cnt: int) -> pd.DataFrame:
    """Get time class checklist options.

    :param: pd.DataFrame df: Dataframe with eco_name and uuid column.
    :param: int cnt: Number of most common ecos to return.
    :return: Dataframe with first `cnt` most common eco_names and their counts.
    :rtype: pd.DataFrame.
    """
    dff = df.groupby('eco_name', as_index=False)['uuid'].count()
    return dff.sort_values('uuid', ascending=False).head(cnt)


def get_result_distribution(df: pd.DataFrame, time_classes: list) -> pd.DataFrame:
    """Calculate result distribution for time_classes. If time_classes is empty, calculate for all of them.

    :param: pd.DataFrame df: Dataframe with eco_name and uuid column.
    :param: list time_classes: List of time_classes.
    :return: Dataframe grouped by result and time_class, with those and count and result type (%) columns.
    :rtype: pd.DataFrame.
    """
    dff = df.copy()
    if time_classes:
        dff = dff[dff['time_class'].isin(time_classes)]
    dff = pd.DataFrame(dff.groupby(['result', 'time_class'], as_index=False)['uuid']
                       .count()
                       .rename(columns={'uuid': 'count'})
                       .reset_index())
    dff['result type (%)'] = 100 * dff['count'] / dff.groupby('time_class')['count'].transform('sum')
    return dff


def get_rated_rating_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Get correlation between rated and unrated games and player's ratings.

    :param: pd.DataFrame df: Dataframe with rated, white_rating and black_rating columns.
    :return: Dataframe grouped by rated with rating_mean column.
    :rtype: pd.DataFrame.
    """
    dff = df.copy()
    dff['rating_mean'] = df.loc[:, ['white_rating', 'black_rating']].sum(axis=1)
    return dff.groupby('rated')['rating_mean'].mean().reset_index()


def get_result_type_count(df: pd.DataFrame) -> pd.DataFrame:
    """Get result_type count per result_type for different results(White, Black, Draw).

    :param: pd.DataFrame df: Dataframe with result, result_type and uuid.
    :return: Dataframe grouped by result and result_type, with count column.
    :rtype: pd.DataFrame.
    """
    dff = df.groupby(['result_type', 'result'], as_index=False)['uuid'].count().rename(columns={'uuid': 'count'})
    return dff.sort_values('count')


def get_result_type_increment_correlation(df: pd.DataFrame, result_types: list) -> pd.DataFrame:
    """Get correlation between game time increment and result_types.

    :param: pd.DataFrame df: Dataframe with increment, result_type and uuid columns.
    :return: Dataframe grouped by increment and result_type, with count and 'result type %' columns,
    sorted by increment. Select all result_types if result_types arg is None.
    :rtype: pd.DataFrame.
    """

    # Obscure solution to prevent the FutureWarning and SettingWithCopyWarning
    df_copy = df.copy()
    df_copy['increment'] = df['increment'].apply(pd.to_numeric)
    dff = df_copy[['increment', 'result_type', 'uuid']]
    dff = dff.loc[dff['increment'] < 60]
    if result_types:
        dff = dff.loc[dff['result_type'].isin(result_types)]

    dff = pd.DataFrame(
        dff.groupby(['increment', 'result_type'], as_index=False).agg(count=('uuid', 'count')).reset_index())
    dff['result type %'] = 100 * dff['count'] / dff.groupby('increment')['count'].transform('sum')
    return dff.sort_values(by=['increment'])
