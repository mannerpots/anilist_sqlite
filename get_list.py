from pip import main
import argparse
from anilist_tools.upcoming_sequels import get_user_id_by_name
from anilist_tools.utils import depaginated_request

STATUSES = ['CURRENT', 'PLANNING', 'COMPLETED', 'DROPPED', 'PAUSED', 'REPEATING']

def get_user_media(user_id, status='COMPLETED', type='ANIME'):
    """Given an AniList user ID, fetch the user's anime list, returning a list of shows and details."""
    query = '''
query ($userId: Int, $type: MediaType, $status: MediaListStatus, $page: Int, $perPage: Int) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            hasNextPage
        }
        # Note that a MediaList object is actually a single list entry, hence the need for pagination
        mediaList(userId: $userId,  type: $type, status: $status, sort: SCORE_DESC) {
            media {
                id
                title {
                    english
                    romaji
                }
                type
                format
                episodes
            }
            score
            status
            progress
            repeat
            startedAt {
                year
                month
                day
            }
            completedAt {
                year
                month
                day
            }
            updatedAt
            notes
            hiddenFromStatusLists
            customLists
        }
    }
}'''

    return [list_entry for list_entry in depaginated_request(query=query,
                                                                      variables={'userId': user_id, 'type': type, 'status': status})]

def main(username: str):
    user_id = get_user_id_by_name(username)
    user_media_list = get_user_media(user_id)
    for entry in user_media_list:
        print(entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given an anilist username, print all the shows they have completed on Anilist.",
        formatter_class=argparse.RawTextHelpFormatter)  # Preserves newlines in help text
    parser.add_argument('-u', '--username', required=False, default='mannerpots',
                        help="User whose list should be checked.")
    args = parser.parse_args()

    main(args.username)