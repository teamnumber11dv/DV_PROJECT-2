"""
Team-11 Project - Football Match Analysis

This script processes StatsBomb JSON data and extracts events for the three visualizations:
1. Turnover Locations
2. Shot Origins
3. Defensive Pressure

Usage:
    python process_statsbomb_data.py --events_path /path/to/events.json --output_dir ./output
"""

import json
import os
import argparse
from collections import defaultdict
from typing import List, Dict, Any

class StatsBombProcessor:
    """Process StatsBomb event data for visualization"""
    
    # Event types for each visualization
    TURNOVER_EVENTS = [
        'Miscontrol',
        'Dispossessed',
        'Duel',
        'Pass',
        'Ball Receipt*',
        'Foul Committed'
    ]
    
    SHOT_EVENTS = ['Shot']
    
    DEFENSIVE_EVENTS = [
        'Pressure',
        'Duel',
        'Interception',
        'Block',
        'Ball Recovery',
        'Clearance',
        'Tackle'
    ]
    
    def __init__(self, events_path: str, lineups_path: str = None):
        """
        Initialize processor with event data
        
        Args:
            events_path: Path to StatsBomb events JSON file
            lineups_path: Optional path to lineups JSON file
        """
        with open(events_path, 'r', encoding='utf-8') as f:
            self.events = json.load(f)
        
        self.lineups = None
        if lineups_path and os.path.exists(lineups_path):
            with open(lineups_path, 'r', encoding='utf-8') as f:
                self.lineups = json.load(f)
    
    def extract_turnovers(self) -> List[Dict[str, Any]]:
        """
        Extract turnover events (miscontrols, dispossessions, lost duels, etc.)
        
        Returns:
            List of turnover events with location and context
        """
        turnovers = []
        
        for event in self.events:
            event_type = event.get('type', {}).get('name', '')
            
            # Miscontrol events
            if event_type == 'Miscontrol':
                turnovers.append(self._create_turnover_event(event, 'Miscontrol'))
            
            # Dispossessed events
            elif event_type == 'Dispossessed':
                turnovers.append(self._create_turnover_event(event, 'Dispossessed'))
            
            # Lost duels
            elif event_type == 'Duel':
                duel = event.get('duel', {})
                if duel.get('outcome', {}).get('name') == 'Lost':
                    turnovers.append(self._create_turnover_event(event, 'Duel Lost'))
            
            # Intercepted passes
            elif event_type == 'Pass':
                pass_data = event.get('pass', {})
                outcome = pass_data.get('outcome', {}).get('name', '')
                if outcome in ['Incomplete', 'Out', 'Pass Offside']:
                    turnovers.append(self._create_turnover_event(event, 'Pass Intercepted'))
            
            # Bad touches
            elif event_type == 'Ball Receipt*':
                outcome = event.get('ball_receipt', {}).get('outcome', {}).get('name', '')
                if outcome == 'Incomplete':
                    turnovers.append(self._create_turnover_event(event, 'Bad Touch'))
        
        return turnovers
    
    def _create_turnover_event(self, event: Dict, turnover_type: str) -> Dict[str, Any]:
        """Create standardized turnover event"""
        location = event.get('location', [60, 40])  # Default to center if missing
        
        return {
            'x': location[0],
            'y': location[1],
            'type': turnover_type,
            'player': event.get('player', {}).get('name', 'Unknown'),
            'team': event.get('team', {}).get('name', 'Unknown'),
            'minute': event.get('minute', 0),
            'second': event.get('second', 0),
            'period': event.get('period', 1),
            'timestamp': event.get('timestamp', '00:00')
        }
    
    def extract_shots(self) -> List[Dict[str, Any]]:
        """
        Extract shot events with xG, location, and outcome
        
        Returns:
            List of shot events
        """
        shots = []
        
        for event in self.events:
            if event.get('type', {}).get('name') == 'Shot':
                shot_data = event.get('shot', {})
                location = event.get('location', [100, 40])
                
                # Determine outcome
                outcome = shot_data.get('outcome', {}).get('name', 'Unknown')
                
                # Map StatsBomb outcomes to our categories
                outcome_mapping = {
                    'Goal': 'Goal',
                    'Saved': 'Saved',
                    'Blocked': 'Blocked',
                    'Off T': 'Off Target',
                    'Post': 'Post',
                    'Wayward': 'Off Target',
                    'Saved Off Target': 'Saved'
                }
                
                mapped_outcome = outcome_mapping.get(outcome, 'Off Target')
                
                shots.append({
                    'x': location[0],
                    'y': location[1],
                    'xG': shot_data.get('statsbomb_xg', 0.0),
                    'outcome': mapped_outcome,
                    'technique': shot_data.get('technique', {}).get('name', 'Unknown'),
                    'body_part': shot_data.get('body_part', {}).get('name', 'Unknown'),
                    'player': event.get('player', {}).get('name', 'Unknown'),
                    'team': event.get('team', {}).get('name', 'Unknown'),
                    'minute': event.get('minute', 0),
                    'second': event.get('second', 0),
                    'period': event.get('period', 1),
                    'timestamp': event.get('timestamp', '00:00')
                })
        
        return shots
    
    def extract_defensive_actions(self) -> List[Dict[str, Any]]:
        """
        Extract defensive events (pressures, tackles, interceptions, etc.)
        
        Returns:
            List of defensive action events
        """
        defensive_actions = []
        
        for event in self.events:
            event_type = event.get('type', {}).get('name', '')
            
            if event_type in self.DEFENSIVE_EVENTS:
                action = self._create_defensive_action(event)
                if action:
                    defensive_actions.append(action)
        
        return defensive_actions
    
    def _create_defensive_action(self, event: Dict) -> Dict[str, Any]:
        """Create standardized defensive action event"""
        event_type = event.get('type', {}).get('name', '')
        location = event.get('location', [60, 40])
        
        # Determine success based on event type
        success = False
        
        if event_type == 'Pressure':
            # Pressure is successful if it leads to a turnover (simplified here)
            success = True  # Default to true, could be refined
        elif event_type == 'Duel':
            duel_outcome = event.get('duel', {}).get('outcome', {}).get('name', '')
            success = duel_outcome in ['Success', 'Won']
        elif event_type == 'Interception':
            interception_outcome = event.get('interception', {}).get('outcome', {}).get('name', '')
            success = interception_outcome in ['Success', 'Won']
        elif event_type == 'Block':
            success = True  # Blocks are generally successful by definition
        elif event_type == 'Ball Recovery':
            success = True
        elif event_type == 'Clearance':
            success = True
        elif event_type == 'Tackle':
            success = True
        
        # Determine defensive zone
        x = location[0]
        zone = 'Low Block'
        if x > 80:
            zone = 'High Press'
        elif x > 40:
            zone = 'Mid Press'
        
        return {
            'x': location[0],
            'y': location[1],
            'type': event_type,
            'success': success,
            'player': event.get('player', {}).get('name', 'Unknown'),
            'team': event.get('team', {}).get('name', 'Unknown'),
            'minute': event.get('minute', 0),
            'second': event.get('second', 0),
            'period': event.get('period', 1),
            'timestamp': event.get('timestamp', '00:00'),
            'zone': zone
        }
    
    def get_match_metadata(self) -> Dict[str, Any]:
        """Extract match metadata from events"""
        if not self.events:
            return {}
        
        first_event = self.events[0]
        
        return {
            'match_id': first_event.get('match_id', 'Unknown'),
            'teams': list(set([e.get('team', {}).get('name', 'Unknown') for e in self.events])),
            'competition': first_event.get('competition', {}).get('name', 'Unknown'),
            'season': first_event.get('season', {}).get('name', 'Unknown')
        }
    
    def save_processed_data(self, output_dir: str):
        """
        Process and save all data for visualizations
        
        Args:
            output_dir: Directory to save processed JSON files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract all event types
        turnovers = self.extract_turnovers()
        shots = self.extract_shots()
        defensive = self.extract_defensive_actions()
        metadata = self.get_match_metadata()
        
        # Save to JSON files
        with open(os.path.join(output_dir, 'turnovers.json'), 'w') as f:
            json.dump(turnovers, f, indent=2)
        
        with open(os.path.join(output_dir, 'shots.json'), 'w') as f:
            json.dump(shots, f, indent=2)
        
        with open(os.path.join(output_dir, 'defensive_actions.json'), 'w') as f:
            json.dump(defensive, f, indent=2)
        
        with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create combined file for easy loading
        combined = {
            'metadata': metadata,
            'turnovers': turnovers,
            'shots': shots,
            'defensive': defensive
        }
        
        with open(os.path.join(output_dir, 'combined_data.json'), 'w') as f:
            json.dump(combined, f, indent=2)
        
        print(f"✓ Processed {len(self.events)} events")
        print(f"✓ Extracted {len(turnovers)} turnover events")
        print(f"✓ Extracted {len(shots)} shot events")
        print(f"✓ Extracted {len(defensive)} defensive actions")
        print(f"✓ Saved to {output_dir}")
        
        return combined


def main():
    parser = argparse.ArgumentParser(description='Process StatsBomb event data')
    parser.add_argument('--events_path', type=str, required=True,
                      help='Path to StatsBomb events JSON file')
    parser.add_argument('--lineups_path', type=str, default=None,
                      help='Path to StatsBomb lineups JSON file (optional)')
    parser.add_argument('--output_dir', type=str, default='./processed_data',
                      help='Output directory for processed data')
    
    args = parser.parse_args()
    
    # Process data
    processor = StatsBombProcessor(args.events_path, args.lineups_path)
    processor.save_processed_data(args.output_dir)


if __name__ == '__main__':
    main()
